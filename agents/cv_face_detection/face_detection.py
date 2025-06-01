import cv2 as cv
import argparse
import zmq
import numpy as np
import time
import  lib.conf as hu_conf
from protoc.hu_msgs_pb import AIDetectionAgent, DetectionData,BoundingBox
from agents.cv_face_detection.yunet import YuNet


def get_timestamp() -> int:
    return round(time.time())


'''
face detection: detect faces from image

code objectives:
    1- get stream from mediamtx
    2- apply face detection
    3- send data over zmq to monitor ai at tcp://localhost:7000

inputs should be:
    1- input stream source
    2- conf threshold
    3- nms threshold
    4- top k
'''



def visualize(image, results, box_color=(0, 255, 0), text_color=(0, 0, 255), fps=None):
    output = image.copy()
    landmark_color = [
        (255,   0,   0), # right eye
        (  0,   0, 255), # left eye
        (  0, 255,   0), # nose tip
        (255,   0, 255), # right mouth corner
        (  0, 255, 255)  # left mouth corner
    ]

    if fps is not None:
        cv.putText(output, 'FPS: {:.2f}'.format(fps), (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, text_color)

    for det in results:
        bbox = det[0:4].astype(np.int32)
        cv.rectangle(output, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), box_color, 2)

        conf = det[-1]
        cv.putText(output, '{:.4f}'.format(conf), (bbox[0], bbox[1]+12), cv.FONT_HERSHEY_DUPLEX, 0.5, text_color)

        landmarks = det[4:14].astype(np.int32).reshape((5,2))
        for idx, landmark in enumerate(landmarks):
            cv.circle(output, landmark, 2, landmark_color[idx], 2)

    return output



parser = argparse.ArgumentParser(description='Face Detection Agent with inputs: input_stream_source')

parser.add_argument('--input_stream_source',type=str, 
                    help='input stream source',default='rtsp://localhost:8554/android-wifi')
parser.add_argument('--channel',type=str, 
                    help='channel for zmq',default='face_detection_default_channel')
parser.add_argument('--conf_threshold', type=float, default=0.9,
                    help='Usage: Set the minimum needed confidence for the model to identify a face, defauts to 0.9. Smaller values may result in faster detection, but will limit accuracy. Filter out faces of confidence < conf_threshold.')
parser.add_argument('--nms_threshold', type=float, default=0.3,
                    help='Usage: Suppress bounding boxes of iou >= nms_threshold. Default = 0.3.')
parser.add_argument('--top_k', type=int, default=5000,
                    help='Usage: Keep top_k bounding boxes before NMS.')

args = parser.parse_args()

model = YuNet(modelPath='agents/cv_face_detection/face_detection_yunet_2023mar.onnx',
                inputSize=[320, 320],
                confThreshold=args.conf_threshold,
                nmsThreshold=args.nms_threshold,
                topK=args.top_k,
                backendId=cv.dnn.DNN_BACKEND_OPENCV,
                targetId=cv.dnn.DNN_TARGET_CPU)

cap = cv.VideoCapture('rtsp://localhost:8554/android-wifi')
if not cap.isOpened():
    print("Error: Cannot open webcam.")
    exit()
    
w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
model.setInputSize([w, h])

context = zmq.Context()
pub_socket = context.socket(zmq.PUB)
socket_address = hu_conf.get_zmq_conf()['ai_monitor_xsub_socket']
pub_socket.connect(socket_address)

current_time=0 
last_process=0
process_time =0
while True:
    
    # t1 = time.time()
    hasFrame, frame = cap.read()
    if not hasFrame:
        print('No frames grabbed!')
        break
    
    current_time = time.time()
    # print(process_time)
    if (current_time- last_process) < process_time * 2:
        continue
    last_process = time.time()
    start_process = time.time()
    results = model.infer(frame) 
    details = []
    for res in results:
        bounding_box = BoundingBox(x=int(res[0]),y=int(res[1]),w=int(res[2]),h=int(res[3]))
        detail = DetectionData(class_name='face',bounding_box=bounding_box,confidence=res[-1])
        details.append(detail)
        
        
    ai_detection_result = AIDetectionAgent(model_name='face_detection',timestamp=get_timestamp(),source_name=args.input_stream_source,details=details)
    channel = args.channel
    pub_socket.send_multipart([channel.encode('utf-8'),ai_detection_result.SerializeToString()])
    # print(ai_detection_result)
    # cv.imshow('image' ,visualize(frame, results))
    # cv.imshow('image2' ,frame)
    
    end_process = time.time()
    process_time = end_process - start_process
    # if cv.waitKey(1) == ord('q'):
    #     break
    
    
cv.destroyAllWindows()


# import cv2

# cap = cv2.VideoCapture('rtsp://localhost:8554/android-wifi')
# while True:
#     _, frame = cap.read()
#     cv2.imshow('im', frame)
    
#     if cv2.waitKey(1) == ord('q'):
#         break
    
# cv2.destroyAllWindows()