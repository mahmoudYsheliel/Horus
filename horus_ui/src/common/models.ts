export type PanelName = 'settings' | 'monitor' | 'agent' |  'none'
export type LogLevel = 'INFO' | 'DEBUG' | 'WARN' | 'ERROR' | '';
export interface LogMsg {
    datetime?: string;
    source?: string;
    level: LogLevel;
    msg: string;
};

export interface ConnectionParam{
    address: string
    username: string
    password: string
    channel:string
}

export interface CameraConfig{
    source_id:string
    soource_type:string
    source_name: string
    enable_recording:boolean
    connection_params:ConnectionParam
}

export const filters = [
    { name: 'gaussian_blur', out: '/gb' },
    { name: 'sharpen', out: '/sh' },
    { name: 'edge_detect', out: '/ed' },
  ] as const;

export type FilterTypeOut = typeof filters[number];

export interface FilterConfig{
    filter_type:FilterTypeOut
    input_src:string[]
    filter_params:Object
}

export const ZMQ={
    monitor_pull_socket: 'tcp://127.0.0.1:6000',
    monitor_rep_socket: 'tcp://127.0.0.1:6001'
}