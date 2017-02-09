#!/usr/bin/python

'''Defines the Sink class, which converts received bits back into a
more usable format (e.g., into a file, an image, etc.).

Currently short, because we aren't yet sending files and images.
'''

import numpy
import sys

from source import Source

class Sink:
    def __init__(self, source):
        '''Source that this Sink is based on.'''

        self.src_type = source.type # not used yet
        self.n_bits = source.n_bits # expected number of bits

        self.received_text = None

    def process(self, received_bits):
        '''Process the received bits.'''

        # Chop off any extra bits (usually represents silence at the
        # end of the transmission)
        if len(received_bits) < self.n_bits:
            sys.stderr.write("Warning: Received fewer bits than expected\n")
        else:
            received_bits = received_bits[:self.n_bits]

        if self.src_type == Source.TEXT:
            self.received_text = self.get_text(received_bits)

        return numpy.array(received_bits, dtype=int)

    def get_text(self, bits):
        '''Returns the text represented by the array of bits (assumes that
        bits was created by a Source reading a text file.'''
        text = []
        intbits = numpy.array([], dtype=numpy.uint8)
        for i in xrange(len(bits)/8):
            intbits = numpy.append(intbits, self.bits2int(bits[i*8:(i+1)*8]))
        for c in intbits:
            text.append(chr(c))
        return  "".join([t for t in text])

    def bits2int(self, bits):
        '''Converts a bit to an integer, so that we can get the ASCII
        encoding.'''
        out = 0
        for ix in xrange(len(bits)):
            out += bits[ix] * (2**(len(bits) - 1 - ix))
        return int(out)

