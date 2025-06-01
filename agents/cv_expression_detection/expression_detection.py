import cv2 as cv
import argparse
import zmq
import numpy as np
import time
import lib.conf as hu_conf
from protoc.hu_msgs_pb import AIDetectionAgent, DetectionData, BoundingBox
from agents.cv_expression_detection.yunet import YuNet
from agents.cv_expression_detection.facial_fer_model import FacialExpressionRecog



def get_timestamp() -> int:
    return round(time.time())


def visualize(image, det_res, fer_res, box_color=(0, 255, 0), text_color=(0, 0, 255)):

    output = image.copy()
    landmark_color = [
        (255, 0, 0),  # right eye
        (0, 0, 255),  # left eye
        (0, 255, 0),  # nose tip
        (255, 0, 255),  # right mouth corner
        (0, 255, 255)   # left mouth corner
    ]

    for ind, (det, fer_type) in enumerate(zip(det_res, fer_res)):
        bbox = det[0:4].astype(np.int32)
        fer_type = FacialExpressionRecog.getDesc(fer_type)
        # print("Face %2d: %d %d %d %d %s." % (ind, bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3], fer_type))
        cv.rectangle(output, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), box_color, 2)
        cv.putText(output, fer_type, (bbox[0], bbox[1] + 12), cv.FONT_HERSHEY_DUPLEX, 0.5, text_color)
        landmarks = det[4:14].astype(np.int32).reshape((5, 2))
        for idx, landmark in enumerate(landmarks):
            cv.circle(output, landmark, 2, landmark_color[idx], 2)
    return output


def process(detect_model, fer_model, frame):
    h, w, _ = frame.shape
    detect_model.setInputSize([w, h])
    dets = detect_model.infer(frame)

    if dets is None:
        return False, None, None

    fer_res = np.zeros(0, dtype=np.int8)
    for face_points in dets:
        fer_res = np.concatenate((fer_res, fer_model.infer(frame, face_points[:-1])), axis=0)
    return True, dets, fer_res


detect_model = YuNet(modelPath='agents/cv_expression_detection/face_detection_yunet_2023mar.onnx')

fer_model = FacialExpressionRecog(modelPath='agents/cv_expression_detection/facial_expression_recognition_mobilefacenet_2022july.onnx',
                                      backendId=cv.dnn.DNN_BACKEND_OPENCV,
                                      targetId=cv.dnn.DNN_TARGET_CPU)




parser = argparse.ArgumentParser(description='Expression Detection Agent with inputs: input_stream_source')

parser.add_argument('--input_stream_source',type=str, 
                    help='input stream source',default='rtsp://localhost:8554/android-wifi')
parser.add_argument('--channel',type=str, 
                    help='channel for zmq',default='expression_detection_default_channel')

args = parser.parse_args()



cap = cv.VideoCapture('rtsp://localhost:8554/android-wifi')
if not cap.isOpened():
    print("Error: Cannot open webcam.")
    exit()
    
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
    
    

    #     # Get detection and fer results
    status, dets, fer_res = process(detect_model, fer_model, frame)

    # if status:
    #     # Draw results on the input image
    #     frame = visualize(frame, dets, fer_res)

    # # Visualize results in a new window
    # cv.imshow('FER Demo', frame)


    details = []
    for res,fer in zip(dets,fer_res):
        bounding_box = BoundingBox(x=int(res[0]),y=int(res[1]),w=int(res[2]),h=int(res[3]))
        detail = DetectionData(class_name=FacialExpressionRecog.getDesc(fer),bounding_box=bounding_box,confidence=res[-1])
        details.append(detail)
    
    ai_detection_result = AIDetectionAgent(model_name='expression_detection',timestamp=get_timestamp(),source_name=args.input_stream_source,details=details)
    channel = args.channel
    pub_socket.send_multipart([channel.encode('utf-8'),ai_detection_result.SerializeToString()])


    
    end_process = time.time()
    process_time = end_process - start_process
    if cv.waitKey(1) == ord('q'):
        break
    
    
cv.destroyAllWindows()


