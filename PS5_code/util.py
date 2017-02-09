#!/usr/bin/python

'''Various utility functions, including modulate.'''

import math
import numpy
import operator

def modulate(fc, samples, sample_rate):
    '''Modulate a series of samples using a given frequency and sample rate.'''
    args = numpy.arange(0, len(samples)) * fc * 2.0 * math.pi / sample_rate
    return samples*numpy.cos(args)

def bits_to_samples(bits, spb, v0, v1):
    '''Convert an array of bits to samples by expanding each bit to spb
    samples.  v0 and v1 define the voltage levels for 0 and 1,
    respectively.'''
    samples = [0.0]*len(bits)*spb
    for i in range(len(bits)):
        v = v1 if bits[i] == 1 else v0
        samples[i*spb:(i+1)*spb] = [v] * spb
    return samples

def hamming(s1, s2):
    '''Return the Hamming distance between two bit strings.  If one is
    shorter than the other, return the HD between the first n bits (n =
    length of shorter string) + difference in their length.'''
    l = min(len(s1), len(s2))
    d = abs(len(s1) - len(s2))
    hd = sum(map(operator.xor,s1[:l],s2[:l]))
    return hd + d

def add_arrays(s1, s2):
    '''Adds two numpy arrays together.  If the arrays are of different
    sizes, the sum is performed as if the smaller array were padded
    with 0's at the end.'''
    L = max(len(s1), len(s2))
    a = numpy.append(s1, [0]*(L-len(s1)))
    b = numpy.append(s2, [0]*(L-len(s2)))
    return a + b
