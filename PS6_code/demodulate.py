#!/usr/bin/python

'''Defines different demodulators to use in the demodulation step.'''

import math
import numpy

import util

def envelope_demodulator(samples):
    '''Perform envelope demodulation on a set of samples (i.e., rectify
    the samples).

    Arguments:
    samples -- array of samples to demodulate'''
    return numpy.abs(samples)

def heterodyne_demodulator(samples, sample_rate, carrier_freq):
    '''Return the samples demodulated via heterodyne demodulation, using a
    cosine of the given frequency (carrier_freq is specified in
    hertz).  You may need to convert between continuous-time and
    discrete-time frequencies.'''
    #args = numpy.arange(0, len(samples))*carrier_freq*2.0*math.pi/sample_rate
    return util.modulate(carrier_freq, samples, sample_rate)#samples*numpy.cos(args)

def quadrature_demodulator(samples, sample_rate, carrier_freq):
    '''Return the samples demodulated via quadrature demodulation.'''
    inp = numpy.arange(0, len(samples))*carrier_freq*2.0*math.pi/sample_rate
    args=samples*numpy.exp(1j*inp)
    
##    cos=samples*numpy.cos(inp)
##    sin=1j*samples*numpy.sin(inp)
    return args

