#!/usr/bin/python

'''Defines the AudioChannel class, derived from Channel.  Transmits
and receives a signal over audio via a lot of pyaudio nonsense.'''

import pyaudio
import struct
import sys

from channel import Channel

class AudioChannel(Channel):

    FORMAT = pyaudio.paFloat32
    CHANNELS = 1

    def __init__(self, config):
        self.p = pyaudio.PyAudio()
        self.sample_rate = config.sample_rate
        self.SAMPLES_PER_CHUNK = config.chunk_size
        self.WRITE_BUFFER_PREFILL = config.prefill
        self.verbose = config.verbose

    def xmit_and_recv(self, samples_tx):
        '''Transmit and receive samples over an Audio channel.  Return an
        array of received samples.'''

        # open soundcard channel
        self.soundcard_inout = self.p.open(format = AudioChannel.FORMAT,
                                           channels = AudioChannel.CHANNELS,
                                           rate = self.sample_rate,
                                           input = True,
                                           output = True,
                                           frames_per_buffer = self.SAMPLES_PER_CHUNK)

        # Create the payload chunks
        sample_count = 0
        total_sample_count = 0
        chunk_data = [ "" ]
        chunk_number = 0
        for s in samples_tx:
            chunk_data[ chunk_number ] += struct.pack( 'f', s)
            total_sample_count += 1
            sample_count += 1
            if sample_count == self.SAMPLES_PER_CHUNK:
                chunk_number += 1
                chunk_data.append("")
                sample_count = 0

        samples_rx = []
        max_recv_samples = total_sample_count + 4000
        nsamples = 0

        # Transmit the prefill chunks
        for chunk in chunk_data[:self.WRITE_BUFFER_PREFILL]:
            self.soundcard_inout.write(chunk)

        # Transmit and receive the actual data
        for chunk in chunk_data[self.WRITE_BUFFER_PREFILL:]:

            # Transmit
            self.soundcard_inout.write(chunk) 

            # Receive
            rx_sample_count = 0
            sample_chunk_rx = []
            try:
                sample_chunk_rx.extend( struct.unpack( 'f' * self.SAMPLES_PER_CHUNK, self.soundcard_inout.read( self.SAMPLES_PER_CHUNK ) ) )
                nsamples += self.SAMPLES_PER_CHUNK
                samples_rx.extend(sample_chunk_rx)
            except IOError as e:
                # These errors can generally be ignored, so we don't
                # print them by default
                if self.verbose:
                    sys.stderr.write( "IOError %s\n" % e )

        # Receive any remaining chunks
        while nsamples < max_recv_samples:
            rx_sample_count = 0
            sample_chunk_rx = []
            try:
                sample_chunk_rx.extend( struct.unpack( 'f' * self.SAMPLES_PER_CHUNK, self.soundcard_inout.read( self.SAMPLES_PER_CHUNK ) ) )
                nsamples += self.SAMPLES_PER_CHUNK
                samples_rx.extend(sample_chunk_rx)
            except IOError as e:
                if self.verbose:
                    sys.stderr.write( "IOError %s\n" % e )

        self.soundcard_inout.close()
        return samples_rx
