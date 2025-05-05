import subprocess
import cv2
import argparse
import ast

'''
gaussian blur: filter to add blur to the image
G(x, y) = (1 / (2 * π * σ²)) * e^(-(x² + y²) / (2 * σ²))
I_filtered(x, y) = Σ_{i=-k}^{k} Σ_{j=-k}^{k} G(i, j) ⋅ I(x + i, y + j)

code objectives:
    1- get stream of mediamtx
    2- apply gaussian filter
    3- stream again in different path
    
the file has the following ideas and notes:
    1- using ffmpeg to read raw data from process stdin
    2- mediamtx works as server for this ffmpeg
    3- '-tune', 'zerolatency' makes the stream has zerolatency
    4- '-re' causes the stream to lag and get damages
    5- frame rate and image size should be the same in both ffmpeg configurations and camera capture configurations
    6- '-pix_fmt', 'bgr24' without this input image will be destroyed 
inputs should be:
    1- input stream source
    2- outout stream source
    3- kernal width
    4- kernal height
    5- sigma
    
'''
parser = argparse.ArgumentParser(description="Gaussian Blur Filter with inputs: input_stream_source, output_stream_source, kernal_size, sigma")

parser.add_argument('--input_stream_source', type=str, help='input stream source', default='rtsp://localhost:8554/android-wifi')
parser.add_argument('--output_stream_source', type=str, help='output stream source', default='rtsp://localhost:8554/android-wifi/gaussian_blur')
parser.add_argument('--kernal_width', type=int, help='gaussian blur filter kernal width', default=5)
parser.add_argument('--kernal_height', type=int, help='gaussian blur filter kernal height', default=5)
parser.add_argument('--sigma', type=float, help='gaussian blur filter std', default=2)
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
    '-s', f'{int(w)}*{int(h)}',     # Set frame size
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

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break
    # Send frame to FFmpeg process
    try:
        frame = cv2.resize(frame,(int(w),int(h)))
        filtered_frame = cv2.GaussianBlur(frame,(args.kernal_width,args.kernal_height), sigmaX=args.sigma, sigmaY=args.sigma)
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
