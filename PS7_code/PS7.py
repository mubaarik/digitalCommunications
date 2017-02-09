import argparse

from PS7_wsim import *
from PS7_tdma import *
from PS7_aloha import *
from PS7_csma import *
from PS7_cw import *

class TDMAWirelessNetwork(WirelessNetwork):
    def __init__(self, n, ptime, load, retry, skew, simtime):
        self.n_nodes = n
        WirelessNetwork.__init__(self, n, "TDMA", ptime, "exponential", load, retry, "None",
                                 skew, 0, simtime)
    def make_node(self,loc,retry):
        return TDMANode(loc,self,retry)

class AlohaWirelessNetwork(WirelessNetwork):
    def __init__(self, n, ptime, load, retry, backoff,
		 skew, pmax, pmin, simtime):
        self.pmax = pmax
        self.pmin = pmin
        WirelessNetwork.__init__(self, n, "Aloha", ptime,"exponential", load, retry, backoff,
                                 skew, 0, simtime)

    def make_node(self,loc,retry):
        return AlohaNode(loc,self,retry)

class CSMAWirelessNetwork(WirelessNetwork):
    def __init__(self,n,ptime,load,retry,backoff,
		 skew,pmax,pmin,simtime):
        self.pmax = pmax
        self.pmin = pmin        
        WirelessNetwork.__init__(self, n, "CSMA", ptime, "exponential", load, retry, backoff, skew, 0, simtime)

    def make_node(self,loc,retry):
        return CSMANode(loc,self,retry)

class CSMACWWirelessNetwork(WirelessNetwork):
    def __init__(self, n, ptime, load,retry,backoff,
		 skew,cwmin,cwmax,simtime):
        self.cwmin = cwmin
        self.cwmax = cwmax      
        WirelessNetwork.__init__(self, n, "WinCSMA", ptime, "exponential", load, retry, backoff,
                                 skew,0, simtime)

    def make_node(self,loc,retry):
        return CSMACWNode(loc,self,retry)

def run(wnet, opt):
    if opt.topo:
        sim = NetSim()
        sim.SetNetwork(wnet)
        sim.MainLoop()
    else:
        wnet.step(opt.simtime)
        if args.gui:
            plot_data(wnet)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gui", action="store_true", default=False, help="show GUI")
    parser.add_argument("-n", "--numnodes", type=int, default=16, help="number of nodes")
    parser.add_argument("-t", "--simtime", type=int, default=10000, help="simulation time")
    parser.add_argument("-b", "--backoff", default='Mine', help="backoff scheme (Mine, None)")
    parser.add_argument("-r", "--retry", action="store_true", default=False, help="show GUI")
    parser.add_argument("-s", "--size", type=int, default=1, help="packet size (in time units)")
    parser.add_argument("-P", "--pmax", type=float, default=1.0, help="max probability of xmission")    
    parser.add_argument("-p", "--pmin", type=float, default=0.0, help="min probability of xmission")    
    parser.add_argument("-l", "--load", type=int, default=100, help="total load % (in pkts/timeslot)")

    parser.add_argument("-k", "--skew", action="store_true", default=False, help="skew source loads")
    parser.add_argument("-W", "--cwmax", type=int, default=1024, help="CW max")
    parser.add_argument("-w", "--cwmin", type=int, default=1, help="CW min")
    parser.add_argument("-m", "--mac", type=str, default="tdma", choices=["tdma", "aloha", "csma", "cw"])
    parser.add_argument("-G", "--topo", action="store_true", default=False, help="show interactive GUI")

    args = parser.parse_args()

    if args.mac == "tdma":
        print "Protocol: TDMA"
        wnet = TDMAWirelessNetwork(args.numnodes, args.size, args.load, args.retry, 
                                                 args.skew,args.simtime)

        run(wnet, args)

    elif args.mac == "aloha":
        print "Protocol: Stabilized ALOHA"
        wnet = AlohaWirelessNetwork(args.numnodes, args.size, args.load, args.retry, args.backoff,
                                    args.skew, args.pmax, args.pmin, args.simtime)
        run(wnet, args)

    elif args.mac == "csma":
        print "Protocol: CSMA"
        wnet = CSMAWirelessNetwork(args.numnodes, args.size, args.load, args.retry, args.backoff,
                               args.skew, args.pmax, args.pmin, args.simtime)
        run(wnet, args)
    elif args.mac == "cw":
        print "Protocol: CSMA/CW"
        wnet = CSMACWWirelessNetwork(args.numnodes, args.size, args.load, args.retry, args.backoff,
                                      args.skew,args.cwmin,args.cwmax,args.simtime)
        run(wnet, args)
    else:
        print "Invalid MAC protocol"

