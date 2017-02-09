import sys, time
import audio
from link_defs import * # link parameters
import numpy as np

# Main audio channel class - use to send and receive samples
class AudioChannel:
    def __init__( self, samplerate, spc, prefill ):
        self.id = "Audio"
        self.samplerate = samplerate

    def xmit_and_recv( self, samples_tx ):
        samples_tx = np.r_[np.array(samples_tx), np.zeros(4000)]
        return list(audio.play_and_record(samples_tx, self.samplerate))

    def xmit(self, samples):
        audio.play(np.array(samples_tx), self.samplerate)

    def recv(self, duration):
        return list(audio.record(duration*self.samplerate, self.samplerate))
