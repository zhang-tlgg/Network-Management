import psutil
import time

def get_net_speed(interval):
    net_msg = psutil.net_io_counters()
    bytes_sent, bytes_recv = net_msg.bytes_sent, net_msg.bytes_recv
    time.sleep(interval)
    net_msg = psutil.net_io_counters()
    bytes_sent2, bytes_recv2 = net_msg.bytes_sent, net_msg.bytes_recv
    bytes_sent3 = bytes_sent2 - bytes_sent
    bytes_recv3 = bytes_recv2 - bytes_recv
    return bytes_sent3, bytes_recv3

class Flow():
    def __init__(self):
        net_msg = psutil.net_io_counters()
        self.bytes_sent_init = self.bytes_sent_last = net_msg.bytes_sent
        self.bytes_recv_init = self.bytes_recv_last = net_msg.bytes_recv
    
    def stopwatch(self):
        '''
        bytes_sent, bytes_recv, bytes_sent_s, bytes_recv_s
        '''
        net_msg = psutil.net_io_counters()
        bytes_sent_new, bytes_recv_new = net_msg.bytes_sent, net_msg.bytes_recv
        bytes_sent_s = bytes_sent_new - self.bytes_sent_last
        bytes_recv_s = bytes_recv_new - self.bytes_recv_last
        bytes_sent = bytes_sent_new - self.bytes_sent_init
        bytes_recv = bytes_recv_new - self.bytes_recv_init
        self.bytes_sent_last = bytes_sent_new
        self.bytes_recv_last = bytes_recv_new
        # 单位 KBytes
        return bytes_sent, bytes_recv, bytes_sent_s, bytes_recv_s

if __name__  ==  '__main__':
    while True:
        x1, x2 = get_net_speed(1)
        print("↑{:.6f} KBytes/s   ↓{:.6f} KBytes/s".format(x1/1024, x2/1024))

