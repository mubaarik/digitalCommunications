#!/usr/bin/python

'''Defines the AbstractChannel class, for simulating zero-mean
Gaussian noise on a channel.'''

import math
import numpy

from channel import Channel

class AbstractChannel(Channel):
    '''Model a channel that adds zero-mean Gaussian noise.  Can also add a
    custom unit sample response for the channel, as well as a custom
    delay.
    '''

    def __init__(self, variance, h, lag):
        self.variance = variance
        self.h = h # unit sample response
        self.lag = lag

    def xmit_and_recv(self, samples):
        '''Adds a sample from a zero-mean Gaussian distribution to each
        element in samples after convolving with the unit sample
        response and adding the specified channel delay.
        self.variance controls the variance of the noise distribution.
        If variance is zero, the result will just be the convolution
        with h.
        '''
        conv_samples = numpy.convolve(self.h, samples)
        lag_samples = numpy.append([0]*self.lag, conv_samples) # add lag
        if self.variance <= 0:
            return lag_samples
        noisy_samples = lag_samples + numpy.random.normal(0.0, math.sqrt(self.variance), len(lag_samples))
        return noisy_samples
