#!/usr/bin/python

'''Defines the Sink class, which converts received bits back into a
more usable format (e.g., into a file, an image, etc.).

Currently short, because we aren't yet sending files and images.
'''

import numpy
import sys

class Sink:
    def __init__(self, source):
        '''Source that this Sink is based on.'''

        self.src_type = source.type # not used yet
        self.n_bits = source.n_bits # expected number of bits

    def process(self, received_bits):
        '''Process the received bits.'''

        # Chop off any extra bits (usually represents silence at the
        # end of the transmission)
        if len(received_bits) < self.n_bits:
            sys.stderr.write("Warning: Received fewer bits than expected\n")
        else:
            received_bits = received_bits[:self.n_bits]

        return numpy.array(received_bits, dtype=int)
