import os
import sys
import time

import lib.log as hu_log
import lib.conf as hu_conf
from protoc.hu_msgs_pb import (
    LogLevel,
)


def __rtsp_link(address: str, channel: str, username: str, password: str) -> str:
    return f"rtsp://{username}:{password}@{address}{channel}"


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Invalid CLI Arguments, Usage: python ffmpeg_record.py <stream_source_id>')
        sys.exit(1)

    stream_source_id = sys.argv[1]
    stream_source = hu_conf.get_stream_sources_conf().get(stream_source_id, None)
    if not stream_source:
        print('Invalid stream_source_id')
        sys.exit(1)

    source_name = stream_source['source_name']
    connection_params = stream_source['connection_params']
    source_link = __rtsp_link(**connection_params)
    recording_duration = hu_conf.get_settings()['recording_duration']

    try:
        while True:
            hu_log.add_log(msg='Starting Recording Session', level=LogLevel.INFO, src=f"ffmpeg_record.{source_name}")
            os.system(f'ffmpeg -i {source_link} -acodec copy -vcodec copy -f segment -segment_time {recording_duration} -reset_timestamps 1 -strftime 1 "data/recordings/{source_name}_%Y-%m-%d_%H-%M-%S.mkv"')
            hu_log.add_log(msg='Recording Session Stopped', level=LogLevel.WARNING, src=f"ffmpeg_record.{source_name}")
            time.sleep(5)

    except KeyboardInterrupt:
        hu_log.add_log(msg='Recording Session Stopped', level=LogLevel.WARNING, src=f"ffmpeg_record.{source_name}")
        sys.exit(0)
