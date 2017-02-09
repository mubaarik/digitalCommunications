#!/usr/bin/python

'''Defines different filters to use in the filtering step.'''

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
