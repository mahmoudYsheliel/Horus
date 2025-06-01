import zmq
import lib.conf as hu_conf
import lib.log as hu_log
from protoc.hu_msgs_pb import LogMsg, LogLevel
from protoc.hu_msgs_pb import AIDetectionAgent
############################## xsub/xpub ##############################

# '''
# Senario1: 
#     - centeral point receives from multi pubs and forward to multi subs
#'''

# context = zmq.Context()
# xsub = context.socket(zmq.XSUB)
# xsub.bind('tcp://127.0.0.1:7000')

# xsub.send(b'\x01')

# xpub = context.socket(zmq.XPUB)
# xpub.bind('tcp://127.0.0.1:7001')

# print("Proxy with logging started...")



# # ####### just connect the two ports
# zmq.proxy(xsub,xpub)

# ####### this part to process in middle of xsub xpub
# poller = zmq.Poller()
# poller.register(xsub, zmq.POLLIN)
# poller.register(xpub, zmq.POLLIN)

# while True:
#     socks = dict(poller.poll())
    
#     # From Publisher to Subscriber
#     if xsub in socks and socks[xsub] == zmq.POLLIN:
#         msg = xsub.recv_multipart()
#         print(f"Forwarding PUB → SUB: {msg}")
#         xpub.send_multipart(msg)

#     # From Subscriber to Publisher (subscription messages)
#     if xpub in socks and socks[xpub] == zmq.POLLIN:
#         sub_msg = xpub.recv()
#         print(f"Subscription update: {sub_msg}")
#         xpub.send(sub_msg)



############################## pull push /pub ##############################

# '''
# Senario2: 
#     - centeral point receives from multi pushs and forward to multi subs
# '''

# context = zmq.Context()
# pull = context.socket(zmq.PULL)
# pull.bind('tcp://*:7000')

# pub = context.socket(zmq.PUB)
# pub.bind('tcp://*:7001')

# print("Proxy with logging started...")

# ####### just connect the two ports
# #zmq.proxy(xsub,xpub)


# while True:
#     msg = pull.recv_multipart()
#     print(f"Forwarding PULL → SUB: {msg}")
#     pub.send_multipart(msg)






############################################################################
############################## IMPLEMENTATION ##############################
############################################################################

SERVICE_NAME = 'AI_monitor_service'
def main():
    zmq_conf = hu_conf.get_zmq_conf()

    context = zmq.Context()
    xsub = context.socket(zmq.XSUB)
    xsub.bind(zmq_conf['ai_monitor_xsub_socket'])
    xsub.send(b'\x01')
    xpub = context.socket(zmq.XPUB)
    xpub.bind(zmq_conf['ai_monitor_xpub_socket'])

    log_msg = LogMsg(timestamp=hu_log.timestamp(),log_level=LogLevel.INFO,src = SERVICE_NAME,msg='Starting AI Monitor...')
    hu_log.print_log(log_msg)
    zmq.proxy(xsub,xpub)
    


    
if __name__ == '__main__':
    main()