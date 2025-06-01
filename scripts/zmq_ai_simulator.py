import zmq
import time
import threading
import random


############################## xsub/xpub ##############################

# '''
# for senarios: Senario1
#     - 3 senders and two listners
# '''
# context = zmq.Context()

# pub_socket1 = context.socket(zmq.PUB)
# pub_socket1.connect("tcp://localhost:7000")  # Connect to proxy's XSUB
# pub_socket2 = context.socket(zmq.PUB)
# pub_socket2.connect("tcp://localhost:7000")  # Connect to proxy's XSUB
# pub_socket3 = context.socket(zmq.PUB)
# pub_socket3.connect("tcp://localhost:7000")  # Connect to proxy's XSUB

# sub_1_2 = context.socket(zmq.SUB)
# sub_1_2.connect('tcp://127.0.0.1:7001')
# sub_1_2.setsockopt_string(zmq.SUBSCRIBE, 'topic1')
# sub_1_2.setsockopt_string(zmq.SUBSCRIBE, 'topic3')
# sub_1_3 = context.socket(zmq.SUB)
# sub_1_3.connect('tcp://127.0.0.1:7001')
# sub_1_3.setsockopt_string(zmq.SUBSCRIBE, 'topic2')
# sub_1_3.setsockopt_string(zmq.SUBSCRIBE, 'topic3')

# senders = [pub_socket1,pub_socket2,pub_socket3]
# topics = ["topic1","topic2","topic3"]

# def send_thread():
#     while True:
#         rand = random.randint(0,2)
#         msg = f"{topics[rand]}"
#         senders[rand].send_string(msg)
#         print('sent: ' , msg)
#         time.sleep(5)

# def receive1_thread():
#     while True:
#         msg = sub_1_2.recv_string()
#         print('received from sub1: ' ,msg)
        
# def receive2_thread():
#     while True:
#         msg = sub_1_3.recv_string()
#         print('received from sub2: ', msg)
        
# s_thread = threading.Thread(target=send_thread)
# s_thread.daemon = True  # Ensure it will exit when the main program ends
# s_thread.start()

# r1_thread = threading.Thread(target=receive1_thread)
# r1_thread.daemon = True
# r1_thread.start()

# r2_thread = threading.Thread(target=receive2_thread)
# r2_thread.daemon = True
# r2_thread.start()  

# while True:
#     time.sleep(1)  



############################## pull push /pub ##############################

# '''
# for senarios: Senario2
#     - 3 senders and two listners
# '''
# context = zmq.Context()

# push_socket1 = context.socket(zmq.PUSH)
# push_socket1.connect("tcp://localhost:7000")  # Connect to proxy's XSUB
# push_socket2 = context.socket(zmq.PUSH)
# push_socket2.connect("tcp://localhost:7000")  # Connect to proxy's XSUB
# push_socket3 = context.socket(zmq.PUSH)
# push_socket3.connect("tcp://localhost:7000")  # Connect to proxy's XSUB

# sub_1_2 = context.socket(zmq.SUB)
# sub_1_2.connect('tcp://127.0.0.1:7001')
# sub_1_2.setsockopt_string(zmq.SUBSCRIBE, 'topic1')
# sub_1_2.setsockopt_string(zmq.SUBSCRIBE, 'topic3')
# sub_1_3 = context.socket(zmq.SUB)
# sub_1_3.connect('tcp://127.0.0.1:7001')
# sub_1_3.setsockopt_string(zmq.SUBSCRIBE, 'topic2')
# sub_1_3.setsockopt_string(zmq.SUBSCRIBE, 'topic3')

# senders = [push_socket1,push_socket2,push_socket3]
# topics = ["topic1","topic2","topic3"]

# def send_thread():
#     while True:
#         rand = random.randint(0,2)
#         msg = f"{topics[rand]}"
#         senders[rand].send_string(msg)
#         print('sent: ' , msg)
#         time.sleep(5)

# def receive1_thread():
#     while True:
#         msg = sub_1_2.recv_string()
#         print('received from sub1: ' ,msg)
        
# def receive2_thread():
#     while True:
#         msg = sub_1_3.recv_string()
#         print('received from sub2: ', msg)
        
# s_thread = threading.Thread(target=send_thread)
# s_thread.daemon = True  # Ensure it will exit when the main program ends
# s_thread.start()

# r1_thread = threading.Thread(target=receive1_thread)
# r1_thread.daemon = True
# r1_thread.start()

# r2_thread = threading.Thread(target=receive2_thread)
# r2_thread.daemon = True
# r2_thread.start()  

# while True:
#     time.sleep(1)  











############################################################################
############################## IMPLEMENTATION ##############################
############################################################################

context = zmq.Context()

pub_socket1 = context.socket(zmq.PUB)
pub_socket1.connect("tcp://localhost:7000")  # Connect to proxy's XSUB
pub_socket2 = context.socket(zmq.PUB)
pub_socket2.connect("tcp://localhost:7000")  # Connect to proxy's XSUB
pub_socket3 = context.socket(zmq.PUB)
pub_socket3.connect("tcp://localhost:7000")  # Connect to proxy's XSUB

sub_1_2 = context.socket(zmq.SUB)
sub_1_2.connect('tcp://127.0.0.1:7001')
sub_1_2.setsockopt_string(zmq.SUBSCRIBE, 'topic1')
sub_1_2.setsockopt_string(zmq.SUBSCRIBE, 'topic3')
sub_1_3 = context.socket(zmq.SUB)
sub_1_3.connect('tcp://127.0.0.1:7001')
sub_1_3.setsockopt_string(zmq.SUBSCRIBE, 'topic2')
sub_1_3.setsockopt_string(zmq.SUBSCRIBE, 'topic3')

senders = [pub_socket1,pub_socket2,pub_socket3]
topics = ["topic1","topic2","topic3"]

def send_thread():
    while True:
        rand = random.randint(0,2)
        msg = f"{topics[rand]}"
        senders[rand].send_string(msg)
        print('sent: ' , msg)
        time.sleep(5)

def receive1_thread():
    while True:
        msg = sub_1_2.recv_string()
        print('received from sub1: ' ,msg)
        
def receive2_thread():
    while True:
        msg = sub_1_3.recv_string()
        print('received from sub2: ', msg)
        
def main():
    s_thread = threading.Thread(target=send_thread)
    s_thread.daemon = True  # Ensure it will exit when the main program ends
    s_thread.start()

    r1_thread = threading.Thread(target=receive1_thread)
    r1_thread.daemon = True
    r1_thread.start()

    r2_thread = threading.Thread(target=receive2_thread)
    r2_thread.daemon = True
    r2_thread.start()  


if __name__ == '__main__':
    main()
    while True:
        time.sleep(1)  
