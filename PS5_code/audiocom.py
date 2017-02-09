#!/usr/bin/python

'''Defines main() for Audiocom, which parses arguments and calls
run().  run() constructs an array of bits, which are pre-pended with a
preamble, converted to samples, modulated, and sent across the
channel.  On the receiving end, samples are demodulated and filtered,
digitized, and converted back to their original source.'''

import argparse
import numpy
import sys

import graphs
import util

from audio_channel import AudioChannel
from abstract_channel import AbstractChannel
from config import Config
from preamble import Preamble
from receiver import Receiver
from sender import Sender
from sink import Sink
from source import Source

def run(config):
    '''Primary Audiocom functionality.'''

    # Create the preamble to pre-pend to the transmission
    preamble = Preamble(config)

    # Create a source
    source = Source(config)
    frequency = config.channel
    print "Channel: %d Hz" % frequency
    print "\n".join(["\t%s" % source])

    # Create the Sender for this Source.  Process the bits to get
    # modulated samples.
    sender = Sender(frequency, preamble, config)
    sender.set_source(source)
    modulated_samples = sender.modulated_samples()

    # Create the channel
    if config.bypass:
        channel = AbstractChannel(config.bypass_noise, config.bypass_h)
    else:
        channel = AudioChannel(config)

    # Transmit and receive data on the channel.  The received samples
    # (samples_rx) have not been processed in any way.
    samples_rx = channel.xmit_and_recv(modulated_samples)
    print 'Received', len(samples_rx), 'samples'

    r = Receiver(frequency, preamble, config)
    try:
        # Call the main receiver function.  The returned array of bits
        # EXCLUDES the preamble.
        bits  = r.process(samples_rx)

        # Push into a Sink so we can convert back to a useful payload
        # (this step will become more useful when we're transmitting
        # files or images instead of just bit arrays)
        sink = Sink(source)
        received_payload = sink.process(bits)
        print "Received %d data bits" % len(received_payload)
 
        if len(received_payload) > 0:
            # Output BER
            hd = util.hamming(received_payload, source.payload)
            ber = float(hd)/len(received_payload)
            print 'BER:', ber
        else:
            print 'Could not recover transmission.'

    except Exception as e:
        # In general, this is a fatal exception.  But we'd still like
        # to look at the graphs, so we'll continue with that output
        print '*** ERROR: Could not detect preamble. ***'

    # Plot graphs if necessary
    if config.graphs:

        try:
            len_demod = config.spb * (len(received_payload) + preamble.preamble_data_len())
        except:
            # If we didn't receive the payload, make a reasonable guess for the number of bits
            len_demod = config.spb * (config.n_bits + preamble.preamble_data_len())

        if config.src_type == Source.U:
            demod_samples = r.graph_info.demod_samples
            plotrange = preamble.preamble_data_len()*config.spb
            graphs.plot_samples(demod_samples[plotrange:len_demod], 'unit-step response', show=True)

        else:
            graphs.plot_graphs(r.graph_info.demod_samples[:len_demod], r.graph_info.hist_samples[:len_demod], config.spb, preamble)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # Source and Sink options
    parser.add_argument("-S", "--src", type=str, default='random', help="payload (0, 1, step, random)")
    parser.add_argument("-n", "--nbits", type=int, default=512, help="number of data bits")

    # Phy-layer Transmitter and Receiver options
    parser.add_argument("-r", "--samplerate", type=int, default=48000, help="sample rate (Hz)")
    parser.add_argument("-i", "--chunksize", type=int, default=256, help="samples per chunk (transmitter)")
    parser.add_argument("-p", "--prefill", type=int, default=60, help="write buffer prefill (transmitter)")
    parser.add_argument("-s", "--spb", type=int, default=512, help="samples per bit")
    parser.add_argument("-c", "--channel", type=int, default=1000, help="carrier frequency (Hz)")
    parser.add_argument("-G", "--gap", type=int, default=500, help="channel gap (Hz)") # not used in PS5
    parser.add_argument("-q", "--silence", type=int, default=80, help="#samples of silence at start of preamble")
    parser.add_argument("-C", "--carrierpreamble", action="store_true", help="detect preamble over carrier, not baseband") # not used in PS5
    parser.add_argument("-t", "--threshold", type=float, help="threshold value")
    parser.add_argument("-w", "--window", type=float, default=.5, help="window for subsample")

    # Modulation (signaling) and Demodulation options
    parser.add_argument("-k", "--keytype", type=str, default="on_off", help="keying (signaling) scheme")
    parser.add_argument("-d", "--demod", type=str, default="envelope", help="demodulation scheme")
    parser.add_argument("-f", "--filter", type=str, default="avg", help="filter type (avg, lp)")
    parser.add_argument("-o", "--one", type=float, default=1.0, help="voltage level for bit 1")
    parser.add_argument("-z", "--zero", type=float, default=0.0, help="voltage level for bit 0 (ignored unless key type is custom)")

    # AbstractChannel options
    parser.add_argument("-a", "--abstract", action="store_true", help="use bypass channel instead of audio")
    parser.add_argument("-v", type=float, default=0.00, help="noise variance (for bypass channel)")
    parser.add_argument("-u", "--usr", type=str, default='1', help="unit step & sample response (h)")
    parser.add_argument("-e", "--usrlen", type=int, default=1, help="length of unit step response")

    # Miscellaneous
    parser.add_argument("-g", "--graph", action="store_true", help="show graphs")
    parser.add_argument("--verbose", action="store_true", help="verbose debugging")

    args = parser.parse_args()

    config = Config(args)
    print config # useful output

    # Go!
    run(config)
