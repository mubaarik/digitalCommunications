from PS7_wsim import *
from PS7 import *

def test_collisions(wnet):
    for node in wnet.nlist:
        if node.stats.collisions > 0: 
            return False
    return True

def tdma_tests():
    failure = False
    warning = False
    # -t 2000
    wnet = TDMAWirelessNetwork(16, 1, 100, False, False, 2000)
    wnet.step(wnet.config.simtime, do_output=False)
    if not test_collisions(wnet):
        print "TDMA: Collision in baseline test (parameters: -t 2000)"
        failure = True
    # -t 14000 -s 7
    wnet = TDMAWirelessNetwork(16, 7, 100, False, False, 14000)
    wnet.step(wnet.config.simtime, do_output=False)
    if not test_collisions(wnet):
        print "TDMA: Collision in packet size test (parameters: -t 14000 -s 7)"
        failure = True
    # -n 20 -k
    wnet = TDMAWirelessNetwork(20, 1, 100, False, True, 10000)
    wnet.step(wnet.config.simtime, do_output=False)
    if not test_collisions(wnet):
        print "TDMA: Collision in skewed load test (parameters: -n 20 -k)"
        failure = True
    wnet = TDMAWirelessNetwork(16, 1, 100, False, False, 2000)
    wnet.step(wnet.config.simtime, do_output=False)
    f = wnet.fairness(0)
    u = 1.0*wnet.stats.success*wnet.config.ptime/wnet.time
    if u < .9:
        print "Warning: TDMA utilization was %f; expected a value above .9 (parameters were -t 2000)" % u
        warning = True
    if f < .98:
        print "Warning: TDMA fairness was %f; expected a value near 1 (parameters were -t 2000)" % f
        warning = True

    if not failure and not warning:
        print "TDMA tests passed"
    elif not failure:
        print "TDMA is collision-free, but fairness and/or utilization appear low"


def aloha_tests():
    warning = False
    wnet = AlohaWirelessNetwork(16, 1, 100, True, 'Mine', False, 1, 0, 10000)
    wnet.step(wnet.config.simtime, do_output=False)
    f = wnet.fairness(0)
    u = 1.0*wnet.stats.success*wnet.config.ptime/wnet.time
    if u < .37:
        print "Warning: ALOHA utilization is %f; expected a value above .37 (parameters were -r --pmax=1 --pmin=0 -t 10000)" % u
        warning = True
    if not warning:
        print "ALOHA tests passed"


def csma_tests():
    warning = False
    wnet = CSMAWirelessNetwork(8, 10, 100, True, 'Mine', False, 1, 0, 100000)
    wnet.step(wnet.config.simtime, do_output=False)
    f = wnet.fairness(0)
    u = 1.0*wnet.stats.success*wnet.config.ptime/wnet.time
    if u < .7 or u > .8:
        print "Warning: CSMA utilization is %f; expected a value between .7 and .8 (parameters were -r --pmin=0 --pmax=1 -s 10 -t 100000 -n 8)" % u
        warning = True
    if f < .75 or f > .9:
        print "Warning: CSMA fairness is %f; expected a value between .75 and .9 (parameters were -r --pmin=0 --pmax=1 -s 10 -t 100000 -n 8)" % f
        warning = True

    if not warning:
        print "CSMA tests passed"

def cw_tests():
    warning = False
    wnet = CSMACWWirelessNetwork(16, 10, 100, True, False, False, 1, 256, 100000)
    wnet.step(wnet.config.simtime, do_output=False)
    f = wnet.fairness(0)
    u = 1.0*wnet.stats.success*wnet.config.ptime/wnet.time
    if u < .68:
        print "Warning: CSMA/CW utilization is %f; expected a value near .7 (parameters were r -s 10 -n 16 -t 100000 -W 256)" % u
        warning = True
    if f < .89:
        print "Warning: CSMA/CW fairness is %f; expected a value near .9 (parameters were r -s 10 -n 16 -t 100000 -W 256)" % f
        warning = True

    if not warning:
        print "CSMA/CW tests passed"


if __name__ == "__main__":
    tdma_tests()
    aloha_tests()
    csma_tests()
    cw_tests()
