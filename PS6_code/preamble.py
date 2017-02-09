import math
import numpy
import util

class Preamble:
    '''
    This class defines the preamble that appears at the beginning of
    every transmission.  The preamble is comprised of a known bit
    sequence, possibly preappended with some samples of silence.
    '''

    def __init__(self, config):
        '''
        config contains the config options for this system.  Preamble
        gets the number of silent samples, if any, from this.
        '''
        self.data = [1,0,1,1,0,1,1,1,0,0,0,1,1,1,1,1,0,0,1,1,0,1,0,1] # barker sequence
        if config is None:
            self.silence = 0
        else:
            self.silence = config.n_silent_samples
        self.preamble = numpy.append([0]*self.silence, self.data)

    def preamble_data_len(self):
        '''
        Returns the length of the preamble data bits
        '''
        return len(self.data)

    def detect(self, demodulated_samples, receiver, offset_hint, zero, one):
        '''
        Detects the preamble in an array of demodulated samples.

        Arguments:
        demodulated_samples = numpy.array of demodulated samples

        receiver = Receiver associated with the reception of the
        demodulated samples.  Used to access the samples per bit,
        sample rate, and carrier frequency of this data.

        offset_hint = our best guess as to where the first 1 bit in
        the samples begins

        zero = best guess for V_0 for these samples
        one = best guess for V_1 for these samples

        Returns:
        The index (as an int) into demodulated_samples where the
        preamble is most likely to start.
        '''

        samples=util.bits_to_samples(self.data, receiver.spb, zero, one)
        modulated=util.modulate(receiver.fc, samples, receiver.sample_rate)
        pream_demod=receiver.demodulate_and_filter(modulated)
        
        start=max(0, offset_hint-len(pream_demod))
        
        end=min((len(demodulated_samples)), (3*len(pream_demod)+offset_hint))
        
        max_c=self.max_correlation_index(pream_demod, demodulated_samples[start:end])
       # print max_c
        return max_c+start

    def max_correlation_index(self, x, y):
        from numpy import linalg as la
        import numpy as np
        '''
        Calculate correlation between two arrays.
        
        Arguments:
        x, y: numpy arrays to be correlated

        Returns:
        - If len(x) == 0 or len(x) > len(y), returns 0
        - Else, returns the index into y representing the most-likely
          place where x begins.  "most-likely" is defined using the
          normalized dot product between x and y
        '''
        index=0
        correlation=0
        if len(x)==0 or len(x)>=len(y):
            index=0
        
        else:
            for i in range(len(y)-len(x)):
                dot=np.dot(x, y[i:(len(x)+i)])
                normal=float(la.norm(y[i:(len(x)+i)])*la.norm(x))
                cor=dot/normal
                
                if cor>correlation:
                    correlation=cor
                    index=i
        return index

if __name__ == "__main__":
    # A simple test for your max_correlation_index function.  This
    # tests your code on the arrays [0.2, 0.4, 0.6, 0.8] and [0.1,
    # -0.05, 0.05, 0.08, 0.14, 0.22, 0.4, 0.8, 0.1, 1.0].  Your code
    # should return the index 2, because the subsequence [0.05, 0.08,
    # 0.15, 0.22] has the highest correlation among all possible
    # choices for x = [0.2, 0.4, 0.6, 0.8].

    p = Preamble(None)
    argmax = p.max_correlation_index([0.2, 0.4, 0.6, 0.8], [0.1, -0.05, 0.05, 0.08, 0.14, 0.22, 0.4, 0.8, 0.1, 1.0])
    if argmax == 2:
        print "Correlate test passed"
    else:
        print "Correlate test not passed; argmax was %d (should be 2)" % argmax
