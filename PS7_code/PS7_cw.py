import random
import numpy
# Feel free to add any imports you might need, and note that you might
# not need to use either of the ones we've provided.

from PS7_wsim import *

class CSMACWNode(WirelessNode):
    def __init__(self,location,network,retry):
        WirelessNode.__init__(self,location,network,retry)
        self.cw = self.network.cwmin # Initialize to cwmin
        self.cwmin = self.network.cwmin
        self.cwmax = self.network.cwmax
        self.t=None
        # Set any additional state or variables here if you need them.

    def channel_access(self, current_time, packet_size):
       
        # TODO: Your code here.  Return true if the node should send a
        # packet in this timeslot (false otherwise).  You can tell if
        # the channel is busy by using the self.network.channel_busy()
        # function.
        if self.t is None:
            self.t = random.randint(1, self.cw)

        if self.t == 0:
            if not self.network.channel_busy():
                self.t = random.randint(1, self.cw)
                return True

        if not self.network.channel_busy():
            self.t -= 1

        return False

    def on_collision(self, packet):
        # TODO: Your code here.  No return value.
        self.cw = min(self.cw*2, self.cwmax)

    def on_success(self, packet):
        # TODO: Your code here.  No return value.
        self.cw = max(self.cw/2, self.cwmin)
