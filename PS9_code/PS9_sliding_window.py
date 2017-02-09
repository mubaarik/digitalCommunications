import random,sys

from PS9_netsim import *
from PS9_util import *

class ReliableSenderNode(AbstractReliableSenderNode):

    def __init__(self,location,qsize,window,address=None,):
        AbstractReliableSenderNode.__init__(self,location,qsize,window,address=address)

    def reset(self):
        Router.reset(self)
        self.srtt = 0
        self.rttdev = 0
        self.timeout = 20    # arbitrary initial value
        # TODO: Your initialization code here, if you need any.  We've
        # already initialized self.srtt, self.rttdev, self.timeout
        # above.
        self.waiting=0
        self.unacked=[]
        self.max_seqnum=0

    # Called every timeslot.  Decides whether to send a new packet, to
    # retransmit, or to do nothing.  If you need to send a packet in
    # this timeslot, use the send_packet() function.
    def reliable_send(self, network_time):
        #if len(self.unacked)>0:
        for unacked in self.unacked:
            if (network_time-unacked.start)>=self.timeout:
                self.unacked.remove(unacked)
                #packet=send_packet(network_time,self.unacked[0].seqnum, self.unacked[0].start)
                self.unacked.append(self.send_packet(network_time,unacked.seqnum, network_time))
                #
        
        if self.waiting<self.window:
            
            self.unacked.append(self.send_packet(network_time,self.max_seqnum, network_time))
           
            self.max_seqnum+=1
            self.waiting+=1
            
    # Invoked whenever an ACK arrives
    def process_ack(self, network_time, acknum, sender_timestamp):
        for packet in self.unacked:
            if packet.seqnum==acknum:
                self.unacked.remove(packet)
                self.waiting-=1
        self.calc_timeout(network_time, sender_timestamp) # Don't delete this!

    # Called whenever an ACK arrives.  Should update the value of
    # self.timeout, as well as the values of self.srtt (smoothed
    # round-trip-time) and self.rttdev (mean linear RTT deviation).
    def calc_timeout(self, time, pkt_timestamp):
        alpha=.125
        beta=.25
        self.srtt=alpha*(time-pkt_timestamp)+(1-alpha)*self.srtt
        dev=abs((time-pkt_timestamp)-self.srtt)
        self.rttdev=beta*dev+(1-beta)*self.rttdev
        self.timeout=self.srtt+4*self.rttdev
       

    # Send a packet at the current time, with specified seqnum,
    # timestamp, and color.  You do not need to edit this method.
    def send_packet(self, time, seqnum, pkt_timestamp, color='black'):
        xmit_packet = self.network.make_packet(
            self.address, self.stream_destination, 'DATA', time, 
            seqnum=seqnum, timestamp=pkt_timestamp, color=color)
        self.forward(xmit_packet)
        return xmit_packet

# ReliableReceiverNode extends Router to implement reliable
# receiver functionality with path vector routing.
class ReliableReceiverNode(AbstractReliableReceiverNode):
    def __init__(self,location,qsize,window,address=None):
        AbstractReliableReceiverNode.__init__(self, location, qsize, window,address=address)
        self.reset()

    def reset(self):
        AbstractReliableReceiverNode.reset(self)
        #TODO: Your code for initializing the receiver, if you need
        #any, should go here
        self.buffer=[]
        self.buffered=0
        

    # Invoked every time the receiver receivers a data packet from the
    # receiver.  Sends an ACK back, and does the rest of the necessary
    # processing.  Use self.send_ack() to send an ACK packet, and
    # self.app_receive() to send a data packet to the receiving
    # application. (self.app_receive() is defined in
    # AbstractReliableSenderNode, though you shouldn't need to know
    # anything about its internals.).  self.app_seqnum will tell you
    # the last sequence number that the receiving application received.
    def reliable_recv(self, sender, network_time, seqnum, packet_timestamp):
        self.send_ack(sender, time, seqnum, packet_timestamp)
        
        self.buffer.append((network_time, seqnum, packet_timestamp))
        
        self.buffered+=1
        
        if seqnum==(self.app_seqnum+1):
            self.app_receive(seqnum, time)
            self.buffer.remove((network_time, seqnum, packet_timestamp))
            self.buffered-=1
        if self.buffered>0:
            self.buffer.sort(key=lambda x:x[1])
            for packet in self.buffer:
                if packet[1]==(self.app_seqnum+1):
                    self.app_receive(packet[1], time)
                    self.buffer.remove(packet)
                    self.buffered-=1

    # Send an ACK packet.  You do not need to modify this method.
    def send_ack(self, sender, time, seqnum, pkt_timestamp):
        ack = self.network.make_packet(self.address, sender, 'ACK', time,
                                       seqnum=seqnum, timestamp=pkt_timestamp,
                                       color='blue')
        self.forward(ack);
