import zmq
import time
import colorama
from datetime import datetime

import lib.log as hu_log
import lib.conf as hu_conf
from protoc.hu_msgs_pb import LogMsg, LogLevel


LOG_TAGS = {
    LogLevel.DEBUG: f"{colorama.Fore.YELLOW}DEBUG{colorama.Style.RESET_ALL}",
    LogLevel.INFO: f"{colorama.Fore.GREEN}INFO{colorama.Style.RESET_ALL}",
    LogLevel.WARNING: f"{colorama.Fore.YELLOW}WARNING{colorama.Style.RESET_ALL}",
    LogLevel.ERROR: f"{colorama.Fore.RED}ERROR{colorama.Style.RESET_ALL}",
    LogLevel.CRITICAL: f"{colorama.Fore.RED}CRITICAL{colorama.Style.RESET_ALL}",
}

zmq_conf = hu_conf.get_zmq_conf()
context = zmq.Context()
monitor_push_socket = context.socket(zmq.PUSH)
monitor_push_socket.connect(zmq_conf['monitor_pull_socket'])


def timestamp() -> int:
    return round(time.time())


def add_log(msg: str, level=LogLevel.DEBUG, src=''):
    log_msg = LogMsg(
        timestamp=timestamp(),
        log_level=level,
        src=src,
        msg=msg,
    )
    monitor_push_socket.send(log_msg.SerializeToString())


def print_log(log_msg: LogMsg):
    log_datetime = datetime.fromtimestamp(log_msg.timestamp)
    fmt_log_msg = f"{LOG_TAGS[log_msg.log_level]}\t{log_datetime.strftime('%Y-%m-%d %H:%M:%S')}\t{log_msg.src}: {log_msg.msg}"
    print(fmt_log_msg)
