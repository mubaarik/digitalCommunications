#!/usr/bin/python

'''Defines the AbstractChannel class, for simulating zero-mean
Gaussian noise on a channel.'''

import math
import numpy

from channel import Channel

class AbstractChannel(Channel):
    '''Model a channel that adds zero-mean Gaussian noise.  Can also add a
    custom unit sample response for the channel.
    '''

    def __init__(self, variance, h):
        self.variance = variance
        self.h = h # unit sample response

    def xmit_and_recv(self, samples):
        '''Adds a sample from a zero-mean Gaussian distribution to each
        element in samples after convolving with the unit sample
        response.  self.variance controls the variance of the noise
        distribution.  If variance is zero, the result will just be
        the convolution with h.
        '''
        conv_samples = numpy.convolve(self.h, samples)
        if self.variance <= 0:
            return conv_samples
        noisy_samples = conv_samples + numpy.random.normal(0.0, math.sqrt(self.variance), len(conv_samples))
        return noisy_samples
