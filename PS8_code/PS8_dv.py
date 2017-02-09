import random,sys,math

from PS8_netsim import *
import PS8_tests

class DVRouter(Router):
    INFINITY = 32

    def send_advertisement(self, time):
        # Do not change this function.  You do not need to modify it.
        adv = self.make_dv_advertisement()
        for link in self.links:
            p = self.network.make_packet(self.address, self.peer(link), 'ADVERT', time, color='red', ad=adv)
            link.send(self, p)        

    def process_advertisement(self, p, link, time):
        # Do not change this function.  You do not need to modify it.
        self.integrate(link, p.properties['ad'])

    def make_dv_advertisement(self):
        # TODO: Your code here
        # Should return a list of the form [(dest1, cost1), (dest2, cost2) ...]
        cost_map=self.cost_table.items()
        return cost_map

    def link_failed(self, dead_link):
        # TODO: Your code here.  No return value.
        #
        # Take the appropriate action given that dead_link has failed.
        # The appropriate action will depend on how you design your
        # protocol.
        #
        # If you need to set a cost fo infinity, use self.INFINITY,
        # not INFINITY.
        for node in self.routes.keys():
            if self.routes[node]==dead_link:
                self.cost_table[node]=self.INFINITY
            
##        dest=self.routes.keys()[self.routes.values().index(dead_link)]
##        self.cost_table[dest]=self.INFINITY

    def integrate(self, link, advertisement):
        # TODO: Your code here.  No return value.  At the end of this
        # function, the variables self.cost_table and self.routes
        # should reflect the current shortest paths.
        # 
        # Recall that self.routes maps addresses to instances of the
        # Link class, and self.cost_table maps addresses to the
        # shortest path cost to that node.
        #
        # link is the link that delivered advertisement.  Use
        # link.cost to determine its cost.
        for dest,costi in advertisement:
            link_cost=link.cost
            if self.routes.has_key(dest):
                if self.routes[dest]==link:
                    #if self.cost_table[dest]>(link_cost+costi):
                    self.cost_table[dest]=(costi+link_cost)
                else:
                    if self.cost_table[dest]>(link_cost+costi):
                        self.cost_table[dest]=(costi+link_cost)
                        self.routes[dest]=link
            else:
                self.cost_table[dest]=(costi+link_cost)
                self.routes[dest]=link
        lost=self.routes.keys()
        for dest in lost:
            
            if self.routes[dest]==link:
                if not dest in dict(advertisement).keys():
                    del self.routes[dest]
                    del self.cost_table[dest]
                
