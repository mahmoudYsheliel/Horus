
import subprocess
import cv2
import argparse
from filters.all_filters import (
    FilterBase,
    default_filter_inputs_map,
    class_map,
    )
'''
filter service: general filter service provider

code objectives:
    1- get stream of mediamtx
    2- apply chain of filter
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
    3- filter
'''


def get_ffmpeg_conf(color_format,width,height,output_path):
    return [
        'ffmpeg',             # The FFmpeg command
        '-y',                 # Overwrite output files without asking
        '-f', 'rawvideo',     # Input format is raw video
        '-vcodec', 'rawvideo',  # Video codec is raw
        '-pix_fmt', color_format,   # Pixel format: BGR (OpenCV default)
        '-s', f'{int(width)}x{int(height)}',     # Set frame size
        # '-r', '30',            # Frame rate: 25 fps
        # commented   '-re',                 # Read the input in real-time
        '-i', '-',             # Input will come from stdin (pipe)
        '-c:v', 'libx264',     # Use x264 codec for output
        '-f', 'rtsp',          # Use RTSP protocol
        '-tune', 'zerolatency',
        '-preset', 'ultrafast',
        '-g', '3',           # Lower GOP (Group of Pictures) for faster first-frame decode
        '-keyint_min', '3',  # Match with GOP
        '-sc_threshold', '0',  # No scene change detection
        output_path  # RTSP server URL
    ]




def parse_filter(filter_args):
    filter_name = filter_args[0]
    params = {}
    for param in filter_args[1:]:
        key, value = param.split('=')
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        params[key] = value
    return {'name': filter_name, 'params': params}


parser = argparse.ArgumentParser()
parser.add_argument('--filter', action='append', nargs='+', help='Define filter and parameters')
parser.add_argument('--input_stream_source', type=str, help='input stream source', default='rtsp://localhost:8554/android-wifi')
parser.add_argument('--output_stream_source', type=str, help='output stream source', default='rtsp://localhost:8554/android-wifi/gaussian_median')
parser.add_argument('--camera_name', type=str, help='name of the camera', default='android-wifi')
args = parser.parse_args()




def main():
    if not args.filter:
        return
    filters_chain = [parse_filter(f) for f in args.filter]
    cap = cv2.VideoCapture(args.input_stream_source)

    initial_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    initial_hright = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    intial_conf = 'bgr24'

    filter_list: list[FilterBase] = []
    for filter in filters_chain:
        filter_name = filter['name']
        if filter_name in class_map.keys():
            params = {**default_filter_inputs_map[filter_name],**filter['params']}
            filter_list.append(class_map[filter_name](**params))
            initial_width,initial_hright,intial_conf = filter_list[-1].calc_out_conf(initial_width,initial_hright,intial_conf)
            
    ffmpeg_cmd = get_ffmpeg_conf(intial_conf,initial_width,initial_hright,args.output_stream_source)

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print('Error reading video')
            return
        for filter in filter_list:
            frame = filter.apply_filter(frame)
        proc.stdin.write(frame.tobytes())


if __name__ =='__main__':
    main()
