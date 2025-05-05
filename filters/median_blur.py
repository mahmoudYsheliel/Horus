import subprocess
import cv2
import argparse
import ast

'''
median filter: filter to remove salt noise
idee: take the median value of the surrounding box to be the value of the cell
I_filtered(x, y) = median{ I(i, j) | (i, j) ∈ Nₖₓₖ(x, y) }


code objectives:
    1- get stream of mediamtx
    2- apply median filter
    3- stream again in different path
    
the file has the following ideas and notes:
    1- using ffmpeg to read raw data from process stdin
    2- mediamtx works as server for this ffmpeg
    3- '-tune', 'zerolatency' makes the stream has zerolatency
    4- '-re' causes the stream to lag and get damages
    5- frame rate and image size should be the same in both ffmpeg configurations and camera capture configurations
inputs should be:
    1- input stream source
    2- outout stream source
    3- kernal size
'''
parser = argparse.ArgumentParser(description="Median Blur Filter with inputs: input_stream_source, output_stream_source, kernal_size, ")

parser.add_argument('--input_stream_source', type=str, help='input stream source', default='rtsp://localhost:8554/android-wifi/gb')
parser.add_argument('--output_stream_source', type=str, help='output stream source', default='rtsp://localhost:8554/android-wifi/gb/mb')
parser.add_argument('--kernal_size', type=int, help='median blur filter kernal size', default=5)
args = parser.parse_args()


cap = cv2.VideoCapture(args.input_stream_source)  # Capture from the default camera (0)

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
    '-pix_fmt', 'bgr24',   # Pixel format: BGR (OpenCV default)
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


# Start the FFmpeg process
proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

# Capture a video stream using OpenCV



while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Send frame to FFmpeg process
    try:
        filtered_frame = cv2.medianBlur(frame,args.kernal_size)
        proc.stdin.write(filtered_frame.tobytes())  # Write frame data to stdin of FFmpeg process
    except BrokenPipeError:
        print("FFmpeg process closed the pipe. Exiting.")
        break
    # Optionally display the video feed locally
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
proc.stdin.close()
proc.wait()
