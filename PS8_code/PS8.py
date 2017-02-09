import argparse

import PS8_dv
import PS8_ls
import PS8_tests

from PS8_netsim import RouterNetwork
from PS8_netsim import NetSim
from PS8_netsim import RandomGraph

class DVRouterNetwork(RouterNetwork):
    def make_node(self, loc, address=None):
        return PS8_dv.DVRouter(loc, address=address)

class LSRouterNetwork(RouterNetwork):
    def make_node(self, loc, address=None):
        return PS8_ls.LSRouter(loc, address=address)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--numnodes", type=int, default=12, help="number of nodes")
    parser.add_argument("-t", "--simtime", type=int, default=2000, help="simulation time")
    parser.add_argument("-r", "--rand", action="store_true", default=False, help="use randomly generated topology")
    parser.add_argument("-p", "--protocol", type=str, default="dv", choices=["dv", "ls"], help="routing protocol (dv or ls)")
    parser.add_argument("-s", "--tests", action="store_true", default=False, help="run tests")

    args = parser.parse_args()

    if args.tests:
        if args.protocol == "dv":
            PS8_tests.verify_routes(DVRouterNetwork)
        elif args.protocol == "ls":
            PS8_tests.verify_routes(LSRouterNetwork)

    else:
        if args.rand == True:
            print "Generating random graph"
            rg = RandomGraph(args.numnodes)
            (NODES, LINKS) = rg.genGraph()
        else:
            print "Using default graph"
            NODES =(('A',0,0), ('B',1,0), ('C',2,0), ('D',3,0),
                    ('E',0,1), ('F',1,1), ('G',2,1), ('H',3,1))
            LINKS = (('A','B'),('A','E'),('B','F'),
                     ('C','D'),('C','F'),('C','G'),
                     ('D','G'),('D','H'),('F','G'),('G','H'))
        if args.protocol == "dv":
            net = DVRouterNetwork(args.simtime, NODES, LINKS, 0)
        elif args.protocol == "ls":
            net = LSRouterNetwork(args.simtime, NODES, LINKS, 0)
        sim = NetSim()
        sim.SetNetwork(net)
        sim.MainLoop()
