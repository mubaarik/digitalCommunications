#!/usr/bin/python

'''Defines different filters to use in the filtering step.'''

import math
import numpy

def averaging_filter(samples, window):
    '''Pass samples through an averaging filter.

    Arguments:
    samples -- samples to average
    window -- window size to use for averaging

    Returns: an array r that is the same size as samples.  r[x] =
    average of samples[x-window] to samples[x], inclusive.  When x <
    window, the averaging window is truncated.
    '''
    x = [0.0]*len(samples)
    for i in range(len(samples)):
        if i-window+1 < 0: # Beginning of the array
            x[i] = numpy.mean(samples[0:i+1])
        else:
            x[i] = numpy.mean(samples[i-window+1:i+1])
    return numpy.array(x)

def low_pass_filter(samples, channel_gap, sample_rate):
    Q_c=channel_gap*numpy.pi/sample_rate
    h=[]
    for i in range(101):
        if i-50==0:
            h.append(Q_c/numpy.pi)
        else:
            nem=numpy.sin(Q_c*(i-50))
            den=numpy.pi*(i-50)
            sinc=nem/den
            h.append(sinc)
    convolution=numpy.convolve(numpy.asarray(h),samples)
    return convolution
