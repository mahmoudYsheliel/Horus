import cv2
import argparse
import zmq
import numpy as np
import time
import sys
import os
from agents.cv_object_tracking.vittrack import VitTrack
from protoc.hu_msgs_pb import TrackObject
from protoc.hu_msgs_pb import BoundingBox, DetectionData, AIDetectionAgent

import lib.conf as hu_conf


def get_timestamp() -> int:
    return round(time.time())

def visualize(image, bbox, score, isLocated, fps=None, box_color=(0, 255, 0), text_color=(0, 255, 0), fontScale=1, fontSize=1):
    output = image.copy()
    h, w, _ = output.shape

    if fps is not None:
        cv2.putText(output, 'FPS: {:.2f}'.format(fps), (0, 30), cv2.FONT_HERSHEY_DUPLEX, fontScale, text_color, fontSize)

    if isLocated and score >= 0.3:
        # bbox: Tuple of length 4
        x, y, w, h = bbox
        cv2.rectangle(output, (x, y), (x + w, y + h), box_color, 2)
        cv2.putText(output, '{:.2f}'.format(score), (x, y + 25), cv2.FONT_HERSHEY_DUPLEX, fontScale, text_color, fontSize)
    else:
        text_size, baseline = cv2.getTextSize('Target lost!', cv2.FONT_HERSHEY_DUPLEX, fontScale, fontSize)
        text_x = int((w - text_size[0]) / 2)
        text_y = int((h - text_size[1]) / 2)
        cv2.putText(output, 'Target lost!', (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX, fontScale, (0, 0, 255), fontSize)

    return output


def reconstruct_rgba_image(arr, width, height):
    img_rgba = arr.reshape((height, width, 4))

    img_bgr = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2BGR)

    return img_bgr



def main(track_object:TrackObject):

    track_model = VitTrack(
        model_path='agents/cv_object_tracking/object_tracking_vittrack_2023sep.onnx',
        backend_id=cv2.dnn.DNN_BACKEND_OPENCV,
        target_id=cv2.dnn.DNN_TARGET_CPU)

    image = reconstruct_rgba_image(np.array(track_object.image_data, dtype=np.uint8), track_object.image_width, track_object.image_height)

    x = track_object.object_x
    y = track_object.object_y
    w = track_object.object_w
    h = track_object.object_h

    video = cv2.VideoCapture(f'rtsp://localhost:8554/{track_object.stream_src}')

    # Init tracker with ROI
    track_model.init(image, (x, y, w, h))
    
    context = zmq.Context()
    pub_socket = context.socket(zmq.PUB)
    socket_address = hu_conf.get_zmq_conf()['ai_monitor_xsub_socket']
    pub_socket.connect(socket_address)
        

    current_time = 0
    last_process = 0
    process_time = 0

    while True:
        has_frame, frame = video.read()
        if not has_frame:
            print('End of video')
            break

        current_time = time.time()
        if (current_time - last_process) < process_time * 2:
            continue
        last_process = time.time()
        start_process = time.time()

        isLocated, bbox, score = track_model.infer(frame)
        # Visualize
        frame = visualize(frame, bbox, score, isLocated)
        #cv2.imshow('VitTrack Demo', frame)
        

        end_process = time.time()
        process_time = end_process - start_process
        
        
        bounding_box = BoundingBox(x=int(bbox[0]),y=int(bbox[1]),w=int(bbox[2]),h=int(bbox[3]))
        detail = DetectionData(class_name='',bounding_box=bounding_box,confidence=score)
        ai_detection_result = AIDetectionAgent(model_name='object_detection',timestamp=get_timestamp(),source_name=track_object.stream_src,details=[detail])
        pub_socket.send_multipart([track_object.track_name.encode('utf-8'),ai_detection_result.SerializeToString()])
        if cv2.waitKey(1) == ord('q'):
            break



cv2.destroyAllWindows()