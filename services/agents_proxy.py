import zmq
import lib.conf as hu_conf



def main():
    zmq_conf = hu_conf.get_zmq_conf()
    context= zmq.Context()
    xsub = context.socket(zmq.XSUB)
    xsub.bind(zmq_conf['ai_monitor_xsub_socket'])
    xsub.send(b'\x01')
    xpub = context.socket(zmq.XPUB)
    xpub.bind(zmq_conf['ai_monitor_xpub_socket'])
    zmq.proxy(xsub,xpub)
    
    
if __name__ == '__main__':
    main()