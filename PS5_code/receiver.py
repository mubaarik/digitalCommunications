#!/usr/bin/python

'''Defines the Receiver class, which performs the primary receiver
functionality (demodulate + filter + digitize).'''

import math
import numpy
import scipy.cluster.vq
import warnings

import demodulate
import filter

from exs import PreambleDetectionError

class GraphInfo:

    def __init__(self):
        pass

class Receiver:

    ENVELOPE = 0
    AVERAGE_FILTER = 1

    def __init__(self, fc, preamble, config):
        self.key_type = config.key_type
        self.fc = fc
        self.gap = config.channel_gap
        self.sample_rate = config.sample_rate
        self.demod_type = config.demod_type
        self.preamble = preamble
        self.filter_type = config.filter_type
        self.spb = config.spb
        self.window_edge = max(0, .5 - (config.subsample_window/2.0))
        self.threshold = config.threshold

        self.graph_info = None

    def demodulate_and_filter(self, samples):
        '''Demodulate and filter the given samples.'''

        if self.demod_type == Receiver.ENVELOPE:
            d_samples = demodulate.envelope_demodulator(samples)

        if self.filter_type == Receiver.AVERAGE_FILTER:
            window_size = int(self.sample_rate/float(self.fc))
            f_samples = filter.averaging_filter(d_samples, window_size)

        return f_samples


    def detect_one(self, demod_samples, thresh, one):
        '''Find the first reliable '1' sample in the array of demodulated
        samples.

        Arguments:
        demod_samples -- the demodulated samples
        thresh -- 0/1 threshold
        one -- voltage level for a 1'''

        # Figure out the averaging window
        left_edge = int(self.window_edge * self.spb)
        right_edge = int((1.0 - self.window_edge) * self.spb)

        # Look for an average that is significantly higher than thresh
        for offset in xrange(len(demod_samples)):
            if offset + right_edge >= len(demod_samples):
                break
            m = numpy.mean(demod_samples[offset + left_edge:offset + right_edge])

            if m > thresh + (one-thresh) / 2:
                return offset

        # If that loop completes, we didn't find a one
        raise PreambleDetectionError("Couldn't detect one")

    def subsample(self, samples):
        '''Subsample the samples array according to the specified window.'''
        start = int(self.window_edge * self.spb)
        end = int((1.0 - self.window_edge) * self.spb)

        subsamp = numpy.array([])

        # For each chunk of spb samples, average the samples in
        # between start and end.
        for i in range(0, len(samples), self.spb):
            if i+start < len(samples):
                subsamp = numpy.append(subsamp, numpy.mean(samples[i+start:i+end]))
        return subsamp

    def process(self, samples):
        '''The physical-layer receive function, which processes the received
        samples by detecting the preamble and then demodulating the
        samples.  Returns the sequence of received bits (after
        demapping).'''

        # Demodulate + filter
        demod_samples = self.demodulate_and_filter(samples)

        # Figure out V_0 and V_1 on the receiving end
        one = max(scipy.cluster.vq.kmeans(demod_samples, 2)[0])
        zero = min(scipy.cluster.vq.kmeans(demod_samples, 2)[0])

        # Set threshold if not set explicitly
        if self.threshold:
            thresh = self.threshold
        else:
            thresh = (one + zero)/2.0

        print '0/1 threshold: %.3f' % thresh

        # Find the sample corresponding to the first reliable '1' bit
        warnings.filterwarnings('error')
        self.graph_info = GraphInfo() # store some information for graphing
        try:
            offset = self.detect_one(demod_samples, thresh, one)
            self.graph_info.demod_samples = demod_samples[offset:]
            self.graph_info.hist_samples = demod_samples[offset + (self.spb):]
        except:
            self.graph_info.demod_samples = demod_samples
            self.graph_info.hist_samples = demod_samples
            raise PreambleDetectionError("Couldn't detect first one")

        # Find the start of the preamble signal (often the same as
        # where the first one is, but not necessarily).
        preamble_signal_start = self.preamble.detect(demod_samples, self, offset, zero, one)

        # Subsample and digitize
        subsamples = self.subsample(demod_samples[preamble_signal_start:])
        bits = self.digitize(subsamples, thresh)

        # Make sure the preample bits exist
        preamble_bit_start = self.preamble.find_preamble(bits)

        if preamble_bit_start >= 0:
            # Calculate SNR
            snr = self.calculate_snr(subsamples)
            if snr > 0.0:
                print "SNR from preamble: %.1f dB" % (10.0*math.log(snr, 10))
            else:
                print "WARNING: Couldn't estimate SNR"

            # Return the received bits minus the preamble
            recd_bits = numpy.array(bits[preamble_bit_start + self.preamble.preamble_data_len():], dtype=int)
            return recd_bits
        else:
            raise PreambleDetectionError("Couldn't detect preamble")

    def digitize(self, samples, thresh):
        '''Digitize an array of samples according to the given threshold.'''
        bits = numpy.array([])
        for s in samples:
            bits = numpy.append(bits, 1 if s > thresh else 0)

        return bits

    def calculate_snr(self, samples):
        '''Calculate the SNR based on the preamble.'''
        barker = self.preamble.data

        zero_samples = numpy.array([samples[i] for i in range(len(barker)) if barker[i] == 0])
        one_samples = numpy.array([samples[i] for i in range(len(barker)) if barker[i] == 1])

        var_0 = numpy.var(zero_samples)
        var_1 = numpy.var(one_samples)

        mu_0 = numpy.mean(zero_samples)
        mu_1 = numpy.mean(one_samples)

        noise = (len(one_samples)*var_1 + len(zero_samples)*var_0) / (len(one_samples) + len(zero_samples))

        if noise != 0:
            return (mu_1 - mu_0)**2 / noise
        else:
            return (mu_1 - mu_0)**2
