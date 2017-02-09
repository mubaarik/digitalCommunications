#!/usr/bin/python

'''Defines different demodulators to use in the demodulation step.'''

import numpy

def envelope_demodulator(samples):
    '''Perform envelope demodulation on a set of samples (i.e., rectify
    the samples).

    Arguments:
    samples -- array of samples to demodulate'''
    return numpy.abs(samples)
