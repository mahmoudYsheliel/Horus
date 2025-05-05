import zmq
import json
import code
import readline
from rlcompleter import Completer

import lib.log as hu_log
import lib.conf as hu_conf
from protoc.hu_msgs_pb import *
from google.protobuf.json_format import MessageToDict


zmq_conf = hu_conf.get_zmq_conf()
context = zmq.Context()

monitor_push_socket = context.socket(zmq.PUSH)
monitor_push_socket.connect(zmq_conf['monitor_pull_socket'])
monitor_req_socket = context.socket(zmq.REQ)
monitor_req_socket.connect(zmq_conf['monitor_rep_socket'])


def __fmt_json(obj: dict):
    print(json.dumps(obj, indent=2))


def __LogMsg() -> LogMsg:
    return LogMsg(timestamp=hu_log.timestamp(), log_level=LogLevel.INFO, src='zmq_cli', msg='ZMQ CLI Test Log Msg')


def __logs():
    monitor_req_socket.send(bytes([MonitorServiceRequest.LOGS_HISTORY]))
    packet = monitor_req_socket.recv()
    logs_msg_list = LogMsgList()
    logs_msg_list.ParseFromString(packet)
    print(logs_msg_list.logs)
    for l in logs_msg_list.logs:
        hu_log.print_log(l)


def __status():
    monitor_req_socket.send(bytes([MonitorServiceRequest.SERVICES_STATUS]))
    packet = monitor_req_socket.recv()
    services_status_map = ServicesStatusMap()
    services_status_map.ParseFromString(packet)
    print(services_status_map)
    __fmt_json(dict(services_status_map.map))
    
def __filters():
    monitor_req_socket.send(bytes([MonitorServiceRequest.FILTER_CONFIG]))
    packet = monitor_req_socket.recv()
    filters_list = Filters()
    filters_list.ParseFromString(packet)
    filters_dict = MessageToDict(filters_list)
    __fmt_json(filters_dict)

    

def __stream_sources():
    monitor_req_socket.send(bytes([MonitorServiceRequest.STREAM_SOURCES]))
    packet = monitor_req_socket.recv()
    stream_sources_list = StreamSources()
    stream_sources_list.ParseFromString(packet)
    stream_sources_dict = MessageToDict(stream_sources_list)
    __fmt_json(stream_sources_dict)

if __name__ == '__main__':
    readline.set_completer(Completer().complete)
    readline.parse_and_bind("tab: complete")
    code.interact(local=locals())
