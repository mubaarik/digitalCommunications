#!/usr/bin/python

'''Defines the Sender class.  The main function of this class is to
take an array of bits (preamble + data) to modulated voltage samples,
which will then be sent over the channel.'''

import numpy
import sys

import util

class Sender:

    ON_OFF = 0
    CUSTOM = 2

    def __init__(self, frequency, preamble, config):
        # Set various options
        self.key_type = config.key_type
        self.fc = frequency
        self.sample_rate = config.sample_rate
        self.preamble = preamble
        self.spb = config.spb

        # Source is set explicitly later, because a single sender
        # can be used for multiple sources.
        self.source = None 

        # Set the appropriate voltage levels for 0 and 1 based on the
        # signaling type
        if self.key_type == Sender.ON_OFF:
            self.v1 = config.one_voltage
            self.v0 = 0.0
        elif self.key_type == Sender.CUSTOM:
            self.v1 = config.one_voltage
            self.v0 = config.zero_voltage

    def set_source(self, src):
        '''Explicitly set the source for this sender.'''
        self.source = src

    def bits_to_samples(self, bits):
        '''Expand bits to samples by replacing each bit with self.spb samples.'''
        return util.bits_to_samples(bits, self.spb, self.v0, self.v1)

    def sample_bits(self):
        '''Returns an array of samples representing the preamble and
        payload.'''
        preamble_bits = self.bits_to_samples(self.preamble.preamble)
        source_bits = self.bits_to_samples(self.source.payload)
        return numpy.append(preamble_bits, source_bits)

    def modulated_samples(self):
        '''Returns the modulated signal (preamble + payload).'''
        samples = self.sample_bits()
        return util.modulate(self.fc, samples, self.sample_rate)
