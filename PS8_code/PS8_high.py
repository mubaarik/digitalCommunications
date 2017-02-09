import PS8_tests
from PS8 import DVRouterNetwork

NODES = (('A',0,0), ('B',1,0), ('C',2,0), ('D',3,0))
LINKS = (('A','B'), ('B','C'), ('C','D'))

net = DVRouterNetwork(4000, NODES, LINKS, 0.0)

infinity = None
for src in net.addresses.keys():
    if infinity == None:
        infinity = net.addresses[src].INFINITY
    else:
        infinity = max(infinity, net.addresses[src].INFINITY)

# add one really high cost link
for l in net.links:
    if (l.end1.address == 'B' and l.end2.address == 'C'):
        l.cost = infinity - 2

print 'Testing a network path with very high cost'
print 'A-----B--------------------------C-----D'
print '   1      self.INFINITY-2           1   '

net.reset()
net.step(count=1000)

routing_table = {}
routing_table['A'] = {'B': ('B',), 'C': ('B',), 'D': (None,)}
routing_table['B'] = {'A': ('A',), 'C': ('C',), 'D': ('C',)}
routing_table['C'] = {'A': ('B',), 'B': ('B',), 'D': ('D',)}
routing_table['D'] = {'A': (None,), 'B': ('C',), 'C': ('C',)}

result = PS8_tests.verify_routing_table(net, routing_table)

if result:
    print "Routing Tables: (format: src, (dst1, link1), (dst2, link2), ...)"
    print "\tA, (B,B), (C,B), (D,None)"
    print "\tB, (A,A), (C,C), (D,C)"
    print "\tC, (A,B), (B,B), (D,D)"
    print "\tD, (A,None), (B,C), (C,C)"
    print 'Route from A<-->D exists in topology but your protocol says it doesn\'t!'
    print 'Why did this happen?  Give your answer in the pset.'
else:
    print "Your code did not give the correct result on this test"
