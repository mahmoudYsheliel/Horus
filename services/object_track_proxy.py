import zmq
import lib.conf as hu_conf
from protoc.hu_msgs_pb import TrackObject
from typing import TypedDict, Dict
import time
from agents.cv_object_tracking import object_tracking
from multiprocessing import Process

class ObjectTrackingAgent(TypedDict):
    object_track_name: list[str] = []
    treminal_id: str


object_track_dict: Dict[str, ObjectTrackingAgent] = {}


def update_object_track_dict(source_name: str, track_name: str):
    all_keyes = object_track_dict.keys()
    if not (source_name in all_keyes):
        object_track_dict[source_name] = ObjectTrackingAgent(object_track_name=[track_name], terminal_id=f"terminal_{time.time()}")
    elif not track_name in object_track_dict[source_name]['object_track_name']:
        object_track_dict[source_name]['object_track_name'].append(track_name)
    else:
        object_track_dict[source_name]['object_track_name'].remove(track_name)
        if len(object_track_dict[source_name]['object_track_name']) == 0:
            del object_track_dict[source_name]



def fire(track_object: TrackObject):
    object_tracking.main(track_object)
def main():

    context = zmq.Context()
    zmq_conf = hu_conf.get_zmq_conf()
    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect(zmq_conf['client_tracking_listner'])

    while True:
        data = pull_socket.recv()
        track_object = TrackObject()
        track_object.ParseFromString(data)
        p = Process(target= fire,args=(track_object,))
        p.start()
        update_object_track_dict(track_object.stream_src,track_object.track_name)
        


if __name__ == '__main__':
    main()
