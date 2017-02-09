import sys
import math
import matplotlib.pyplot as p

x_data = []
y_data = []
y_theory = []

f = open("sliding-data.dat", 'r')
lines = f.readlines()

for line in lines:
    # Each line contains a (loss rate, observed throughput) tuple
    loss_rate, observed_tput = line.rstrip().split()
    per_link_loss_rate = float(loss_rate) # per-link loss rate
    observed_tput = float(observed_tput)  # observed throughput at this particular loss rate

    # For experimental-data plot.  Don't change these.
    x_data.append(per_link_loss_rate)
    y_data.append(observed_tput)

    # TODO: Replace the number 0.0 with the correct theoretical y
    # value.  You may use any of the variables above, or create new
    # ones if you need them (remember that you know the network
    # topology and window size; those are given in the lab write-up).
    theoretical_y_value = 0.0

    y_theory.append(theoretical_y_value)

p.xlabel('Per-link loss probability')
p.ylabel('Throughput (pkts/time slot)')
p.plot(x_data, y_data,label="experiment")
p.plot(x_data, y_theory,label="theory")
p.legend()
p.ylim(0, 1)
p.show()

