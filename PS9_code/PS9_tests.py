import argparse
import PS9

def run_network(net):
    net.reset()
    net.step(net.simtime)
    source = net.find_node(0,0)
    sink = net.find_node(len(net.nlist) - 1, 0)
    totaldrop = 0
    for node in net.nlist: totaldrop = totaldrop + node.qdrop 
    totalloss = 0
    for link in net.links: totalloss = totalloss + link.linkloss 
    tput = float(sink.app_seqnum)/(net.time - 1)
    return (tput, totaldrop, totalloss)


def test_stop_wait_no_loss():
    warning_flag = False
    # numhops, simtime, window, qsize, loss, xrate, bottleneck
    net = PS9.make_network(1, 10000, 1, 10, 0.00, 0.00, 1)
    tput, _, _ = run_network(net)
    if (tput < .49 or tput > .51):
        print "Warning: Throughput should be near .5 with parameters -w 1 -n 1; yours was %f" % tput
        warning_flag = True
    net = PS9.make_network(2, 10000, 1, 10, 0.0, 0.0, 1)
    tput, _, _ = run_network(net)
    if (tput < .24 or tput > .26):
        print "Warning: Throughput should be near .25 with parameters -w 1 -n 2; yours was %f" % tput
        warning_flag = True

    if not warning_flag:
        print "PASSED: Window-size = 1, loss prob = 0"


def test_stop_wait_loss():
    warning_flag = False
    error_flag = False
    net = PS9.make_network(3, 10000, 1, 10, 0.01, 0.00, 1)
    tput, _, _ = run_network(net)
    if (tput < .01):
        print "ERROR: Throughput was %f with parameters -w 1 -n 3 -l .01; should be near .15"
        print "       Are you handling retransmissions?"
        error_flag = True
    if (tput < .15 or tput > .16):
        print "Warning: Throughput should be near .155 with parameters -w 1 -n 3 -l .01; yours was %f" % tput
        print "         Are you setting self.timeout correctly?"
        warning_flag = True
    if not error_flag and not warning_flag:
        print "PASSED: Window-size = 1, loss prob > 0"


def test_sliding_window():

    # Basic test; no loss
    net = PS9.make_network(10, 10000, 20, 1000, 0.0, 0.00, 1)
    tput, _, _ = run_network(net)
    if (tput < .99):
        print "ERROR: Throughput was %f with parameters -w 20 -n 10 -l 0; should be almost 1" % tput
    else:
        print "PASSED: Basic sliding-window test"

    # Large window test
    net = PS9.make_network(10, 10000, 1000, 2000, 0.001, 0.00, 1)
    tput, _, _ = run_network(net)
    if (tput < .9):
        print "ERROR: Throughput was %f with parameters -w 1000 -n 10 -l .001; should be near .96" % tput
        print "       Are you retransmitting packets correctly?  And buffering at the receiver?"
    elif (tput < .94):
        print "WARNING: Throughput was %f with parameters -w 1000 -n 10 -l .001; should be near .96" % tput
    else:
        print "PASSED: Large window test"


if __name__ == "__main__":
    test_stop_wait_no_loss()
    test_stop_wait_loss()
    test_sliding_window()
    print "Disclaimer: We reserve the right to test your code on tests other than these!"
