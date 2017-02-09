import random
import numpy
# Feel free to add any imports you might need, and note that you might
# not need to use either of the ones we've provided.

from PS7_wsim import *

class CSMANode(WirelessNode):
    def __init__(self,location,network,retry):
        WirelessNode.__init__(self,location,network,retry)
        # Initialize local probability of transmission
        self.p = float(self.network.pmax)
        self.pmax = float(self.network.pmax)
        self.pmin = float(self.network.pmin)
        # Set any additional state or variables here if you need them.

    def channel_access(self, current_time, packet_size):
        # TODO: Your code here.  Return true if the node should send a
        # packet in this timeslot (false otherwise).  You can tell if
        # the channel is busy by using the self.network.channel_busy()
        # function.
        send=False
        if random.random()<=self.p:
            if not self.network.channel_busy():
                send=True
        return send 

    def on_collision(self, packet):
        # TODO: Your code here.  No return value.
        self.p=max(self.pmin, self.p/2)

    def on_success(self, packet):
        # TODO: Your code here.  No return value.
        self.p=min(self.pmax, self.p*2)
