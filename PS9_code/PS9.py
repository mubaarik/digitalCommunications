import argparse

from PS9_sliding_window import *

class MyNetwork(RouterNetwork):
    def __init__(self,SIMTIME,NODES,LINKS,WINDOW,QSIZE,LOSSPROB,XRATE,VERBOSE):
        self.qsize = QSIZE
        self.lossprob = LOSSPROB
        self.xrate = XRATE
        self.verbose = VERBOSE
        self.window = WINDOW
        RouterNetwork.__init__(self,SIMTIME,NODES,LINKS)

    def make_node(self,loc,address=None):
        if address == 'S':
            return ReliableSenderNode(loc,self.qsize,self.window,address)
        elif address == 'R':
            return ReliableReceiverNode(loc,self.qsize,self.window,address)
        else:
            if self.xrate == 0.0 or len(NODES) == 2:
                return Router(loc,self.qsize,address=address)            
            if self.xrate > 0.0:
                numhops = len(NODES) - 1
                if address == str(numhops - 1):
                    print 'xtraffic node', address
                    return CrossTrafficNode(loc,self.qsize,address,
                                            self.xrate,'R')
                else:
                    return Router(loc,self.qsize,address=address)

    def make_link(self,n1,n2):
        return LossyLink(n1,n2,self.lossprob)

    # reset network to its initial state
    def reset(self):
        # parent class handles the details
        Network.reset(self)
        # insert a single packet into the network. Since we don't have code
        # to deliver the packet this just keeps the simulation alive...
        src = self.addresses['S']
        src.stream_destination = 'R'
        src.add_packet(self.make_packet('S','R','DATA',1))


def make_network(numhops, simtime, window, qsize, loss, xrate, bottleneck, verbose=False):

    NODES = [('S', 0, 0)]
    LINKS = []
    prevnode = 'S'
    for i in xrange(1, numhops):
        NODES.append((str(i), i, 0))
        LINKS.append((prevnode, str(i)))
        prevnode = str(i)
    NODES.append(('R', numhops, 0))
    LINKS.append((prevnode, 'R'))

    net = MyNetwork(simtime, NODES, LINKS, window, qsize, loss, xrate, verbose)

    bneck_node = net.find_node(numhops-1, 0)
    bneck_link = bneck_node.getlink('R')
    bneck_link.set_rate(bottleneck)

    for node in net.nlist:
        if node.address == 'S':
            if numhops > 1:
                node.routes['R'] = node.getlink('1')
            else:
                node.routes['R'] = node.getlink('R')
            for i in xrange(1, numhops):
                node.routes[str(i)] = node.getlink('1')
        elif node.address == 'R':
            if numhops > 1:
                node.routes['S'] = node.getlink(str(numhops - 1))
            else:
                node.routes['S'] = node.getlink('S')

            for i in xrange(1, numhops):
                node.routes[str(i)] = node.getlink(str(numhops - 1))
        else:
            if node.address == '1':
                node.routes['S'] = node.getlink('S')
            else:
                node.routes['S'] = node.getlink(str(int(node.address) - 1))
            if int(node.address) == numhops - 1:
                node.routes['R'] = node.getlink('R')
            else:
                node.routes['R'] = node.getlink(str(int(node.address) + 1))
                
            for i in xrange(1, numhops):
                if int(node.address) < i:
                    node.routes[str(i)] = node.getlink(str(int(node.address)+1))
                elif int(node.address) > i:
                    node.routes[str(i)] = node.getlink(str(int(node.address)-1))
    return net




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bottleneck", type=float, default=1, help="bottleneck link rate (link to R)")
    parser.add_argument("-l", "--loss", type=float, default=0.00, help="per-link loss prob for DATA and ACK packets")
    parser.add_argument("-n", "--numhops", type=int, default=6, help="number of hops between sender S and receiver R")
    parser.add_argument("-q", "--qsize", type=int, default=10, help="queue size at each link")
    parser.add_argument("-t", "--simtime", type=int, default=10000, help="simulation time")
    parser.add_argument("-x", "--xrate", type=float, default=0.0, help="set cross traffic (pkts/slot)")
    parser.add_argument("-w", "--window", type=int, default=1, help="window size")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="print each DATA/ACK/loss/drop event")
    parser.add_argument("-g", "--gui", action="store_true", default=False, help="show GUI")

    args = parser.parse_args()

    net = make_network(args.numhops, args.simtime, args.window, args.qsize, args.loss, args.xrate, args.bottleneck, verbose=args.verbose)

    if args.gui == True:
        # setup graphical simulation interface
        sim = NetSim()
        sim.SetNetwork(net)
        sim.MainLoop()
    else:
        net.reset()
        net.step(args.simtime)
        source = net.find_node(0,0)
        print "Sender S: srtt %s rttdev %s timeout %.1f" % (source.srtt, source.rttdev, source.timeout)
        sink = net.find_node(args.numhops,0)
        print "Receiver R: throughput %.2f pkts/timeslot recd %d in time %d" % (float(sink.app_seqnum)/(net.time - 1), sink.app_seqnum, net.time-1)
        totaldrop = 0
        for node in net.nlist: totaldrop = totaldrop + node.qdrop 
        totalloss = 0
        for link in net.links: totalloss = totalloss + link.linkloss 
        print "\tqueue drops: %d pkts link losses %d pkts" % (totaldrop, totalloss)
