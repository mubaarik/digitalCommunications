from PS9_netsim import *

# AbstractReliableSenderNode extends Router and implements many of the
# functions of a reliable sender.  The core functionality is
# implemented in ReliableSenderNode (see PS9_sliding_window.py)
class AbstractReliableSenderNode(Router):
    def __init__(self,location,qsize,window,address=None):
        Router.__init__(self,location,qsize,address=address)
        self.window = window            # sliding window size
        self.stream_destination = None  # where to send reliable packet stream
        self.reset()

    def __repr__(self):
        return 'ReliableSenderNode<%s>' % str(self.address)

    # GUI options
    def OnClick(self,which):
        if which == 'left':
            if self.network.time > 1:
                print Node.__repr__(self) + "srtt %.1f rttdev %.1f timeout %.1f" % (self.srtt, self.rttdev, self.timeout)
            else:
                print self.__repr__()

    # Transmit a packet
    def transmit(self, time):
        Router.transmit(self,time)
        if self.stream_destination is not None and time >= 1:
            self.reliable_send(time)

    # Process an ACK (and ignore any other packet type)
    def receive(self,p,link,time):
        if p.type == 'ACK':
            acknum = p.properties.get('seqnum', None)
            pkt_timestamp = int(p.properties.get('timestamp', None))
            if self.network.verbose:
                print "t=%d %s received ACK %d" % (time, self.address, acknum)
            self.process_ack(time, acknum, pkt_timestamp)

    # Implemented by ReliableSenderNode
    def reset(self):
        pass

    # Implemented by ReliableSenderNode
    def reliable_send(self, time):
        pass

    # Implemented by ReliableSenderNode
    def process_ack(self, time, acknum, timestamp):
        pass

    # Implemented by ReliableSenderNode
    def calc_timeout(self, time, pkt_timestamp):
        pass

    # Implemented by ReliableSenderNode
    def send_packet(self, time, seqnum, pkt_timestamp, color='black'):
        pass


# AbstractReliableReceiverNode extends Router and implements many of the
# functions of a reliable receiver.  The core functionality is
# implemented in ReliableReceiverNode (see PS9_sliding_window.py)
class AbstractReliableReceiverNode(Router):
    def __init__(self,location,qsize,window,address=None):
        Router.__init__(self,location,qsize,address=address)
        self.window = window
        self.reset()

    def __repr__(self):
        return 'ReliableReceiverNode<%s>' % str(self.address)

    # Reset
    def reset(self):
        Router.reset(self)
        self.app_seqnum = 0
        self.lastprinttime = 0

    # GUI
    def OnClick(self,which):
        if which == 'left':
            if self.network.time > 1:
                print Node.__repr__(self) + " received %d (%.2f packets/timestep)" % (self.app_seqnum, float(self.app_seqnum)/(self.network.time - 1))
            else:
                print self.__repr__()

    # Send ACK
    def send_ack(self, sender, time, seqnum, pkt_timestamp):
        pass

    # Receive a packet
    def receive(self, p, link, time):
        seqnum = p.properties.get('seqnum', None)
        pkt_timestamp = p.properties.get('timestamp', None)
        if p.type == 'DATA':
            self.reliable_recv(p.source, time, seqnum, pkt_timestamp)

    # app_receive() should be called by receive() for each data packet that 
    # arrives in order of incrementing sequence number (i.e., without gaps)
    def app_receive(self, seqnum, time):
        try:
            assert seqnum == self.app_seqnum + 1, \
                "ERROR: Expected DATA packet #%d, got #%d" \
                % (self.app_seqnum+1,seqnum)
            if self.network.verbose == True:
                print "t=%d %s app_receive pkt %d" % (time,self.address,seqnum)
                if time - self.lastprinttime >= 100:
                    print "t=%d rcvr %s app_receive %d throughput: %.2f pkts/timestep" % \
                        (time, self.address, self.app_seqnum, float(self.app_seqnum)/(self.network.time - 1))
                    self.lastprinttime = time
        except AssertionError, a:
            print "*BUG* in protocol: %s" % a
        self.app_seqnum = seqnum
