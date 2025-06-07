//monitor_pull_socket: tcp://127.0.0.1:6000
//monitor_rep_socket: tcp://127.0.0.1:6001

import { LogMsg, LogLevel, MonitorServiceRequest, ServicesStatusMap, LogMsgList, Filters,StreamSources,AIDetectionAgent,Agents, TrackObject } from './generated/hu_msgs'
import * as zmq from 'zeromq'

import { BrowserWindow, ipcMain } from 'electron';


const monitor_push = new zmq.Push();
monitor_push.connect('tcp://127.0.0.1:6000')

const monitor_req = new zmq.Request()
monitor_req.connect('tcp://127.0.0.1:6001')

const monitor_ai_sub = new zmq.Subscriber()
monitor_ai_sub.connect('tcp://127.0.0.1:7001')
monitor_ai_sub.subscribe("")

const track_send = new zmq.Push()
track_send.bind('tcp://127.0.0.1:7501')



const log = new LogMsg();
log.timestamp = 1672215379;
log.log_level = LogLevel.INFO;
log.src = 'zmq_cli';
log.msg ="ZMQ CLI Test Log Msg";

export async function ai_agent_subscriber(mainWindow: BrowserWindow){
  for await (const [channel,msg] of monitor_ai_sub){
    const SSM = AIDetectionAgent.deserializeBinary(msg)
    const data = {channel:channel.toString(),data: SSM.toObject()}
    mainWindow.webContents.send('ai_agent',data)
  }
}
export async function send_log() {
  await monitor_push.send(log.serializeBinary())
  return true
}

export async function get_logs() {
  await monitor_req.send(new Uint8Array([MonitorServiceRequest.LOGS_HISTORY]))
  const packet = await monitor_req.receive()

  const SSM = LogMsgList.deserializeBinary(packet[0])
  return SSM.toObject()
 
}


export async function get_status() {
  await monitor_req.send(new Uint8Array([MonitorServiceRequest.SERVICES_STATUS]))
  const packet = await monitor_req.receive()
  const SSM = ServicesStatusMap.deserializeBinary(packet[0])
  return SSM.map
}


export async function get_filters() {
    await monitor_req.send(new Uint8Array([MonitorServiceRequest.FILTER_CONFIG]))
    const packet = await monitor_req.receive()
  
    const SSM = Filters.deserializeBinary(packet[0])
    return SSM.toObject()
}


export async function get_agents() {
  await monitor_req.send(new Uint8Array([MonitorServiceRequest.AGENTS_CONFIG]))
  const packet = await monitor_req.receive()

  const SSM = Agents.deserializeBinary(packet[0])
  return SSM.toObject()
}

export async function get_stream_sources() {
    await monitor_req.send(new Uint8Array([MonitorServiceRequest.STREAM_SOURCES]))
    const packet = await monitor_req.receive()
  
    const SSM = StreamSources.deserializeBinary(packet[0])
    return SSM.toObject()
   
}




export function init_test_zmq(mainWindow: BrowserWindow) {
  ipcMain.handle('get_monitor_status', async () => {
    const value = await get_status()
    return value
  })

  ipcMain.handle('get_monitor_logs', async () => {
    const value = await get_logs()
    return value
  })

  ipcMain.handle('send_log', async () => {
    const value = await send_log()
    return value
  })

  ipcMain.handle('get_filters', async () => {
    const value = await get_filters()
    return value
  })

  ipcMain.handle('get_stream_sources', async () => {
    const value = await get_stream_sources()
    return value
  })
  ipcMain.handle('get_agents', async () => {
    const value = await get_agents()
    return value
  })
  ai_agent_subscriber(mainWindow)



  ipcMain.on('send_track_data',async (_, arg)=>{
    const data = arg.data as TrackObject
    const message = new TrackObject()
    message.image_data = data.image_data
    message.image_height = data.image_height
    message.image_width = data.image_width
    message.object_x = data.object_x
    message.object_y = data.object_y
    message.object_w = data.object_w
    message.object_h = data.object_h
    message.track_name = data.track_name
    message.stream_src = data.stream_src
    await track_send.send(message.serializeBinary())
  })
  

}
