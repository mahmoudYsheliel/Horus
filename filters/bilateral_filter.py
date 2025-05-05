import subprocess
import cv2
import argparse
import ast

'''
bilateral blur: edge-preserving smoothing in image processing.
I_filtered(x, y) = (1 / W_p) * Σ Σ G_s(‖(i, j) - (x, y)‖) * G_r(|I(i, j) - I(x, y)|) * I(i, j)

code objectives:
    1- get stream of mediamtx
    2- apply bilateral filter
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
    4- sigma color
    5- sigma space
    
'''
parser = argparse.ArgumentParser(description="Bilateral Filter with inputs: input_stream_source, output_stream_source, kernal_size, sigma_color, sigma_space")

parser.add_argument('--input_stream_source', type=str, help='input stream source', default='rtsp://localhost:8554/android-wifi')
parser.add_argument('--output_stream_source', type=str, help='output stream source', default='rtsp://localhost:8554/mystream/bf')
parser.add_argument('--kernal_size', type=int, help='gaussian blur filter kernal size', default=3)
parser.add_argument('--sigma_color', type=float, help='gaussian blur filter kernal width', default=5)
parser.add_argument('--sigma_space', type=float, help='gaussian blur filter std', default=2)
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
        filtered_frame = cv2.bilateralFilter(frame,args.kernal_size, args.sigma_color,args.sigma_space)
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
