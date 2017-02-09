#!/usr/bin/python

'''Defines the base class, Channel.'''

class Channel:

    def __init__(self, config):
        pass

    def xmit_and_recv(self, samples):
        '''Return an array of received samples, the result of sending samples
        through the channel.

        Arguments:
        samples -- an array of modulated voltage samples (serve as the
        input to the channel)
        '''
        pass
