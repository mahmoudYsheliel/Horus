import os
import sys
import yaml
import subprocess
import re
import time
from typing import Literal
import lib.log as hu_log
import lib.conf as hu_conf
from protoc.hu_msgs_pb import (
    LogMsg,
    LogLevel,
)

Service = Literal['Filter', 'Agent']


def __ilog(msg: str):
    hu_log.print_log(LogMsg(timestamp=hu_log.timestamp(), log_level=LogLevel.INFO, src='horus_launch', msg=msg))


def __elog(msg: str):
    hu_log.print_log(LogMsg(timestamp=hu_log.timestamp(), log_level=LogLevel.ERROR, src='horus_launch', msg=msg))


def __check_horus_shell() -> bool:
    proc = subprocess.run(['tmux', 'ls'], capture_output=True, text=True)
    if proc.stdout.startswith('no server running'):
        return False
    if 'horus_shell' in proc.stdout:
        return True
    else:
        return False


def __lss(service_name: str) -> str:
    ''' launch service scripts '''
    return f"cd {os.getcwd()} && source scripts/set_env.bash && python services/{service_name}.py"


def __rtsp_link(address: str, channel: str, username: str, password: str) -> str:
    return f"rtsp://{username}:{password}@{address}{channel}"


def __ffmpeg_record(source_link: str, source_name: str):
    return f"python scripts/ffmpeg_record.py {source_link} {source_name}"


def __mmtx_path_params(stream_source: dict, enable_recording=False) -> dict:
    mmtx_path_params = {}
    source_name = stream_source['source_name']
    connection_params = stream_source['connection_params']
    if stream_source['source_type'] == 'RTSP':
        source_link = __rtsp_link(**connection_params)
        mmtx_path_params['source'] = source_link
        if enable_recording:
            mmtx_path_params['runOnInit'] = __ffmpeg_record(source_link, source_name)
    return mmtx_path_params


def __mmtx_path_params_filter(filter_out_channel: str, enable_recording=False) -> dict:
    mmtx_path_params = {}
    source_link = 'rtsp://localhost:8554/' + filter_out_channel
    if enable_recording:
        mmtx_path_params['runOnInit'] = __ffmpeg_record(source_link, filter_out_channel)
    return mmtx_path_params


def launch_service(index: int, service_file: str, params: dict | None, service_type: Service):
    if not __check_horus_shell():
        __elog('No Horus Shell Found')
        sys.exit(1)

    HS_SHELL_ID = f'horus_shell:{index}'
    __ilog(f'Launching Horus {service_type} {index}...')
    os.system(f"tmux new-window -t {HS_SHELL_ID}")
    params_string = ''
    if params:
        for key, value in params.items():
            if isinstance(value,list):
                for val in value:
                    params_string = params_string + f' --{key} {val}'
            else:
                params_string = params_string + f' --{key} {value}'

    run_command = f"cd {os.getcwd()} && source scripts/set_env.bash && python {service_file} {params_string}"
    os.system(f"tmux send-keys -t {HS_SHELL_ID} '{run_command}' C-m")
    __ilog(f'Launching Horus {service_type} ...OK')


def launch_horus_shell():
    if __check_horus_shell():
        __ilog('Killing Old Horus Shell...')
        os.system('tmux kill-session -t horus_shell')
        __ilog('Killing Old Horus Shell...OK')

    __ilog('Launching New Horus Shell...')
    os.system('tmux new-session -d -t horus_shell')
    if __check_horus_shell():
        __ilog('Launching New Horus Shell...OK')
    else:
        __elog('Launching New Horus Shell...ERR')
        sys.exit(1)


def launch_monitor_service():
    if not __check_horus_shell():
        __elog('No Horus Shell Found')
        sys.exit(1)

    HS_SHELL_ID = 'horus_shell:1'
    __ilog('Launching Horus Monitor Service...')
    os.system(f"tmux new-window -t {HS_SHELL_ID}")
    os.system(f"tmux send-keys -t {HS_SHELL_ID} '{__lss('monitor')}' C-m")
    __ilog('Launching Horus Monitor Service...OK')


def launch_ai_monitor_service(shell_id: int):
    if not __check_horus_shell():
        __elog('No Horus Shell Found')
        sys.exit(1)
    HS_SHELL_ID = f'horus_shell:{shell_id}'
    __ilog('Launching Horus AI Monitor Service...')
    os.system(f"tmux new-window -t {HS_SHELL_ID}")
    os.system(f"tmux send-keys -t {HS_SHELL_ID} '{__lss('AI_monitor')}' C-m")
    __ilog('Launching Horus AI Monitor Service...OK')


def launch_mediamtx():
    __ilog('Generating MediaMTX YML Config...')
    # settings = hu_conf.get_settings()
    # enable_recording: bool = settings['enable_recording']
    stream_sources = hu_conf.get_stream_sources_conf()
    filters = hu_conf.get_filters_conf()
    agents = hu_conf.get_agents_conf()
    mediamtx_paths = {}
    for s_src in stream_sources.values():
        enable_recording = s_src['enable_recording']
        mediamtx_paths[s_src['source_name']] = __mmtx_path_params(s_src, enable_recording)

    for out_channel, filter_data in filters.items():
        filter_output_channel = filter_data['camera_name'] + '/' + out_channel
        mediamtx_paths[filter_output_channel] = __mmtx_path_params_filter(filter_output_channel, filter_data['enable_recording'])

    mediamtx_yml = yaml.safe_dump({'paths': mediamtx_paths}, width=1024)
    with open('mediamtx.yml', 'w') as f:
        f.write(mediamtx_yml)
    __ilog('Generating MediaMTX YML Config...OK')

    HS_SHELL_ID = 'horus_shell:2'
    __ilog('Launching Horus MediaMTX Service...')
    os.system(f"tmux new-window -t {HS_SHELL_ID}")
    os.system(f"tmux send-keys -t {HS_SHELL_ID} 'cd {os.getcwd()} && ./mediamtx' C-m")
    __ilog('Launching Horus MediaMTX Service...OK')

    ############ filters up ############
    index = 3
    for _, filter_data in filters.items():
        params = {}
        params['camera_name'] = filter_data['camera_name'] 
        params['input_stream_source'] = filter_data['input_src']
        params['output_stream_source'] = filter_data['output_src'] 
        params['filter'] = []
        if len(filter_data['filters_chain']) > 0:
            for filter in filter_data['filters_chain']:
                filter_str = str(filter['name'])
                for filter_conf_key,filter_conf_val in filter['params'].items():
                    filter_str +=  ' ' + str(filter_conf_key) + '=' + str(filter_conf_val)
                    
                params['filter'].append(filter_str)
    
        filter_file = f'filters/filter_service.py'
        launch_service(index, filter_file, params, 'Filter')
        index = index + 1

    ############ agents up ############
    launch_ai_monitor_service(index)
    index += 1

    for channel, agent_data in agents.items():
        params = agent_data['agent_params']
        params = {} if not params else params
        params['input_stream_source'] = agent_data['input_src']
        params['channel'] = channel
        agent_path = agent_data['path'] + agent_data['agent']
        agent_file = f'agents/{agent_path}.py'
        launch_service(index, agent_file, params,'Agent')
        index = index + 1


if __name__ == '__main__':
    launch_horus_shell()
    launch_monitor_service()
    launch_mediamtx()
