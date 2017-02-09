#!/usr/bin/python

'''Defines functions for making particular plots.'''

import platform
import math
import numpy
import warnings
import matplotlib

if platform.uname()[0] == 'Darwin':
    matplotlib.use('macosx')

import matplotlib.mlab as mlab
import matplotlib.pyplot as p


def plot_samples(samples, name, spb=None, show=False):
    '''Plot an array of samples.

    Arguments:
    samples -- samples to plot
    name -- title for graph
    spb -- samples per bit
    show -- if true, displays the graph (if false, usually there is a
    separate call to p.show() in a later function)
    '''
    p.title(name)
    p.xlabel('Sample number')
    p.ylabel('Voltage')
    if spb:
        for i in range(0, len(samples), spb):
            p.axvline(i, color='r')
    p.ylim(ymin=min(0, min(samples)))
    p.ylim(ymax=1.5*max(samples))
    p.plot(range(len(samples)), samples)

    if show:
        p.show()
    

def plot_hist(data, name, overlay=False, line=None):
    '''Plot a histogram.  Also output stats about the sample statistics.

    Arguments:
    data -- data to plot
    name -- title of graph
    overlay -- if true, overlay with a best-fit Gaussian
    line -- if exists, plot a line at this x value
    '''

    mean = numpy.mean(data)
    std = numpy.std(data)

    n, bins, patches = p.hist(data, math.sqrt(len(data)), (mean - 3*std, mean + 3*std), normed=True, facecolor='g', alpha=0.75)
    if overlay:
        p.plot(bins, mlab.normpdf(bins, mean, std), 'r--', linewidth=1)
    print 'Sample mean %.2g, sample stddev %.2g, max %.2g, min %.2g' % (mean, std, numpy.max(data), numpy.min(data))
    if line:
        p.axvline(line)
    p.xlabel('Voltage')
    p.ylabel('Prob. density')
    p.title('Histogram of the %s' % name)
    p.grid(True)


def plot_graphs(demod_samples, hist_samples, spb, preamble):
    '''Plot the graphs we use in PS5 (demodulated samples + histogram).'''

    scale = spb/4 - 1
   
    # fix hist_samples to only consider the 1/2 of the samples per bit closest to the center
    header_len = 0
    plotrange = (preamble.preamble_data_len()+header_len)*spb, len(hist_samples)-spb

    hist = hist_samples[plotrange[0]:plotrange[1]]
    hist_samples = []
    for i in xrange(len(hist)/spb):
        hist_samples.extend(hist[int((i+0.25)*spb):int((i+0.75)*spb)])

    p.figure(1)

    # plot the received samples
    p.subplot(211)
    plot_samples(demod_samples[plotrange[0]:plotrange[1]], 'Demodulated Samples', spb=None)
    
    # plot the histogram of demodulated samples in ONE dimension 
    p.subplot(212)
    plot_hist(hist_samples, 'demodulated samples', overlay=True)

    warnings.filterwarnings("ignore")
    p.tight_layout()
    p.show()
