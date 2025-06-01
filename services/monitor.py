import zmq

import lib.log as hu_log
import lib.conf as hu_conf
from protoc.hu_msgs_pb import *


SERVICE_NAME = 'monitor_service'

logs_history = LogMsgList()
services_status_map = ServicesStatusMap()
filter_list = Filters()
stream_sources_list = StreamSources()
agents_list = Agents()


def handle_log_msg(log_msg: LogMsg):
    logs_history.logs.append(log_msg)
    hu_log.print_log(log_msg)


def handle_stream_sources():
    sources = hu_conf.get_stream_sources_conf()
    for src_name, src in sources.items():
        new_src = stream_sources_list.stream_sources[src_name]
        new_src.source_id = str(src['source_id'])
        new_src.source_type = src['source_type']
        new_src.source_name = src['source_name']
        new_src.enable_recording = src['enable_recording']

        connection_params = src['connection_params']
        cp = new_src.connection_params  # <-- get existing connection_params

        cp.address = connection_params['address']
        cp.username = connection_params['username']
        cp.password = str(connection_params['password'])
        cp.channel = connection_params['channel']




def handle_filters():
    filters = hu_conf.get_filters_conf()
    for filter_name, filter in filters.items():
        new_filter = filter_list.filters[filter_name]

        new_filter.camera_name = filter['camera_name']
        new_filter.input_src = filter['input_src']
        new_filter.output_src = filter['output_src']
        new_filter.enable_recording = filter['enable_recording']
        if filter['filters_chain']:
            for single_filter_chain in filter['filters_chain']:
                new_single_filter_chain = SingleFilterChain()
                new_single_filter_chain.name = single_filter_chain['name']
                for k,v in single_filter_chain['params'].items():
                    new_single_filter_chain.params[k] = v
                new_filter.filters_chain.append(new_single_filter_chain)
                
def handle_agents():
    agents = hu_conf.get_agents_conf()
    for agent_name, agent in agents.items():
        new_agent = agents_list.agents[agent_name]
        
        new_agent.agent = agent['agent']
        new_agent.path = agent['path']
        new_agent.input_src = agent['input_src']
        if agent['agent_params']:
            for k,v in agent['agent_params'].items():
                new_agent.agent_params[k] = v
        

def main():
    zmq_conf = hu_conf.get_zmq_conf()
    context = zmq.Context()
    handle_log_msg(LogMsg(timestamp=hu_log.timestamp(), log_level=LogLevel.INFO, src=SERVICE_NAME, msg='Starting Monitor Service...'))

    monitor_pull_socket = context.socket(zmq.PULL)
    monitor_pull_socket.bind(zmq_conf['monitor_pull_socket'])
    monitor_rep_socket = context.socket(zmq.REP)
    monitor_rep_socket.bind(zmq_conf['monitor_rep_socket'])

    poller = zmq.Poller()
    poller.register(monitor_pull_socket, zmq.POLLIN)
    poller.register(monitor_rep_socket, zmq.POLLIN)

    handle_log_msg(LogMsg(timestamp=hu_log.timestamp(), log_level=LogLevel.INFO, src=SERVICE_NAME, msg='Starting Monitor Service...OK'))
    services_status_map.map[SERVICE_NAME] = ServiceStatus.ONLINE
    handle_filters()
    handle_stream_sources()
    handle_agents()
    while True:
        socks = dict(poller.poll())

        if socks.get(monitor_pull_socket) == zmq.POLLIN:
            log_packet = monitor_pull_socket.recv()
            log_msg = LogMsg()
            log_msg.ParseFromString(log_packet)
            handle_log_msg(log_msg)

        if socks.get(monitor_rep_socket) == zmq.POLLIN:
            req_code = monitor_rep_socket.recv()
            if len(req_code) != 1:
                handle_log_msg(LogMsg(timestamp=hu_log.timestamp(), log_level=LogLevel.ERROR, src=SERVICE_NAME, msg='Invalid Monitor Service Request'))
            req_code = req_code[0]

            if req_code == MonitorServiceRequest.LOGS_HISTORY:
                monitor_rep_socket.send(logs_history.SerializeToString())
            elif req_code == MonitorServiceRequest.SERVICES_STATUS:
                monitor_rep_socket.send(services_status_map.SerializeToString())
            elif req_code == MonitorServiceRequest.FILTER_CONFIG:
                monitor_rep_socket.send(filter_list.SerializeToString())
            elif req_code == MonitorServiceRequest.STREAM_SOURCES:
                monitor_rep_socket.send(stream_sources_list.SerializeToString())
            elif req_code == MonitorServiceRequest.AGENTS_CONFIG:
                monitor_rep_socket.send(agents_list.SerializeToString())


if __name__ == '__main__':
    main()
