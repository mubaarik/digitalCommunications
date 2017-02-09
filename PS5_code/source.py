#!/usr/bin/python

'''Defines the Source class, which generates a payload given a
particular source type.  In the future, this class will also take care
of sources such as files, images, etc.'''

import random
import sys

class Source:

    ZEROS = 0
    ONES = 1
    RANDOM = 2
    U = 3

    def __init__(self, config):

        self.type = config.src_type
        self.n_bits = config.n_bits

        # Create the payload
        if self.type == Source.RANDOM: # random bits
            self.payload = [random.randint(0,1) for i in range(self.n_bits)]
        elif self.type == Source.ONES: # all ones
            self.payload = [1] * self.n_bits
        elif self.type == Source.ZEROS: # all zeros
            self.payload = [0] * self.n_bits
        elif self.type == Source.U: # unit step response: 0's then 1's
            self.payload = [0] * (self.n_bits/2) + [1]*(self.n_bits/2)
        else:
            sys.stderr.write("Payload type not supported\n")
            sys.exit(-1)

        # For outputting data types
        self._str_map = {Source.RANDOM: "random", Source.ONES : "all ones", Source.ZEROS : "all zeros", Source.U : "unit step response"}


    def __str__(self, indent=False):
        s = "%sData type: %s\n" % ("\t" if indent else "", self._str_map[self.type])
        s += "%sData size: %d bits\n" % ("\t" if indent else "", len(self.payload))
        return s
