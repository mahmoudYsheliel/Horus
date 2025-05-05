import cv2
import numpy as np
from collections import deque
import subprocess
import argparse

'''
motion filter: filter to detect motion 
idea: get the farame difference between two consecutive frames for certain period of time and sum them
code objectives:
    1- get stream from mediammtx
    2- apply the motion filter
    3- stream again

the file has the following ideas and notes:
    1- using ffmpeg to read raw data from process stdin
    2- mediamtx works as server for this ffmpeg
    3- '-tune', 'zerolatency' makes the stream has zerolatency
    4- '-re' causes the stream to lag and get damages
    5- frame rate and image size should be the same in both ffmpeg configurations and camera capture configurations

notes for the filter:
    1- the frame difference applied on gray level as we are interestead only on the pixel and change value not 3 colors
    2- gaussian blur could be applied but we didn't as it is a separete module
    3- threshold applied to make pixel with certain limits only pass
    4- the idea of the filter comes from vibra

inputs should be:
    1- input stream source
    2- outout stream source
    3- number of frames (buffer size)
    4- threshold value
'''

parser = argparse.ArgumentParser(description="Motion Filter with inputs: input_stream_source, output_stream_source, frame_count, threshhold")

parser.add_argument('--input_stream_source', type=str, help='input stream source', default='rtsp://localhost:8554/android-wifi')
parser.add_argument('--output_stream_source', type=str, help='output stream source', default='rtsp://localhost:8554/mystream/mf')
parser.add_argument('--frame_count', type=int, help='number of frame differences to add', default=5)
parser.add_argument('--threshold', type=int, help='threshold to apply on frame differences sum', default=5)
args = parser.parse_args()


cap = cv2.VideoCapture(args.input_stream_source)  

if not cap.isOpened():
    print("Error: Cannot open webcam.")
    exit()
w = cap.get(3)
h = cap.get(4)
# Define the FFmpeg command to send the video stream
ffmpeg_cmd = [
    'ffmpeg',             # The FFmpeg command
    '-y',                 # Overwrite output files without asking
    '-f', 'rawvideo',     # Input format is raw video
    '-vcodec', 'rawvideo',  # Video codec is raw
    '-pix_fmt', 'gray',   # Pixel format: BGR (OpenCV default)
    '-s', f'{int(w)}*{int(h)}',       # Set frame size
    # '-r', '30',            # Frame rate: 25 fps
    # commented   '-re',                 # Read the input in real-time
    '-i', '-',             # Input will come from stdin (pipe)
    '-c:v', 'libx264',     # Use x264 codec for output
    '-f', 'rtsp',          # Use RTSP protocol
    '-tune', 'zerolatency',
    '-preset', 'ultrafast',
    args.output_stream_source  # RTSP server URL
]


proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

frame_diff_buffer = deque(maxlen=args.frame_count)
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break


    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_diff = cv2.absdiff(prev_gray, gray)
        frame_diff_buffer.append(frame_diff)
        summed_frame_diff = np.zeros_like(frame_diff)
        for diff in frame_diff_buffer:
            summed_frame_diff += diff
        
        proc.stdin.write(summed_frame_diff.tobytes())  # Write frame data to stdin of FFmpeg process
        cv2.imshow('Motion Detection (Summed Over 20 Frames)', summed_frame_diff)
        prev_gray = gray
    except BrokenPipeError:
        print("FFmpeg process closed the pipe. Exiting.")
        break
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()
proc.stdin.close()
proc.wait()
