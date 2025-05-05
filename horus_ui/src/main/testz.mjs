//monitor_pull_socket: tcp://127.0.0.1:6000
//monitor_rep_socket: tcp://127.0.0.1:6001

import { LogMsg, LogLevel, MonitorServiceRequest, ServicesStatusMap, LogMsgList, Filters,StreamSources } from './generated/modulejs/hu_msgs.js'
import * as zmq from 'zeromq'


const monitor_push = new zmq.Push();
monitor_push.connect('tcp://127.0.0.1:6000')

const monitor_req = new zmq.Request()
monitor_req.connect('tcp://127.0.0.1:6001')

// console.log(hu_msgs.LogMsg.encode(hu_msgs.LogMsg.create({ timestamp:1672215379, logLevel:hu_msgs.LogLevel.INFO, src:'zmq_cli', msg:'ZMQ CLI Test Log Msg' })))


const log = new LogMsg();
log.timestamp = 1672215379;
log.log_level = LogLevel.INFO;
log.src = 'zmq_cli';
log.msg ="ZMQ CLI Test Log Msg";

async function send_log() {
  await monitor_push.send(log.serializeBinary())
  return true
}

async function get_logs() {
  await monitor_req.send(new Uint8Array([MonitorServiceRequest.LOGS_HISTORY]))
  const packet = await monitor_req.receive()

  const SSM = LogMsgList.deserializeBinary(packet[0])
  return SSM.toObject()
 
}


async function get_status() {
  await monitor_req.send(new Uint8Array([MonitorServiceRequest.SERVICES_STATUS]))
  const packet = await monitor_req.receive()
  const SSM = ServicesStatusMap.deserializeBinary(packet[0])
  return SSM.map
}


async function get_filters() {
    await monitor_req.send(new Uint8Array([MonitorServiceRequest.FILTER_CONFIG]))
    const packet = await monitor_req.receive()
  
    const SSM = Filters.deserializeBinary(packet[0])
    return SSM.toObject()
   
}

async function get_stream_sources() {
    await monitor_req.send(new Uint8Array([MonitorServiceRequest.STREAM_SOURCES]))
    const packet = await monitor_req.receive()
  
    const SSM = StreamSources.deserializeBinary(packet[0])
    return SSM.toObject()
   
}