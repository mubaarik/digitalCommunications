#!/usr/bin/python

'''Converts commandline arguments into a configuration.'''

import sys

from source import Source
from sender import Sender
from receiver import Receiver

class Config:

    def __init__(self, args):

        # Convert source type to a valid type
        if args.src == "random":
            self.src_type = Source.RANDOM
        elif args.src == "1":
            self.src_type = Source.ONES
        elif args.src == "0":
            self.src_type = Source.ZEROS
        elif args.src == "step":
            self.src_type = Source.U
        else:
            sys.stderr.write("Undefined payload type\n")
            sys.exit()

        # Threshold for threshold detection (usually not set)
        try:
            self.threshold = args.threshold
        except Exception as e:
            self.threshold = None


        # Transmitter/receiver options
        self.n_bits = args.nbits
        self.sample_rate = args.samplerate
        self.chunk_size = args.chunksize
        self.prefill = args.prefill
        self.spb = args.spb
        self.subsample_window = args.window
        self.channel = int(args.channel)
        self.channel_gap = args.gap
        self.n_silent_samples = args.silence
        self.use_carrier_preamble = args.carrierpreamble
        self.one_voltage = args.one
        self.zero_voltage = args.zero


        # Signaling type
        if args.keytype == "on_off":
            self.key_type = Sender.ON_OFF
        elif args.keytype == "custom":
            self.key_type = Sender.CUSTOM
        else:
            sys.stderr.write("Unsupported signaling type\n")
            sys.exit(-1)

        # Demodulation
        if args.demod == 'envelope':
            self.demod_type = Receiver.ENVELOPE
        else:
            sys.stderr.write("Unsupported demodulation type\n")
            sys.exit(-1)

        # Filter
        if args.filter == "avg":
            self.filter_type = Receiver.AVERAGE_FILTER
        else:
            sys.stderr.write("Unsupported filter type\n")
            sys.exit(-1)

        # AbstractChannel options
        self.bypass = args.abstract
        if self.bypass:
            self.bypass_noise = args.v
            hlen = args.usrlen

            if hlen > 1:
                self.bypass_h = [1.0/hlen for i in range(hlen)]
            else:
                self.bypass_h = [float(x) for x in args.usr.split(' ')]

        # Graphs + verbosity
        self.graphs = args.graph
        self.verbose = args.verbose

    def __str__(self):
        s = "Parameters in experiment:\n"
        s += "\tSamples per bit: %d\n" % self.spb
        s += "\tKeying scheme: %s\n" % self.key_type
        s += "\tDemodulation scheme: %s\n" % self.demod_type
        s += "\tChannel type: %s\n" % ('Audio' if not self.bypass else 'Bypass')
        if self.bypass:
            s += '\t  Noise: %s h: [%s]\n' % (self.bypass_noise, self.bypass_h)
        s += "\tFrequency (Hz): %s" % (self.channel)
        return s
