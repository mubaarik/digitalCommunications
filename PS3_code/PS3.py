# This is the template file for 6.02 Viterbi decoding
import numpy,sys
from collections import defaultdict

def convolutional_encode(message, G):
    # K is the constraint length (the length of each generator).  r is
    # the number of generators.
    r, K = G.shape
    message_len = message.size
    # Start off with all zeros
    result = numpy.zeros((r,message_len))
    # Convolve in GF2
    for i in range(r):
        result[i,] = numpy.convolve(G[i,], message)[:message_len] % 2
    # Reshape the array so that we have the type of output we want
    result = result.transpose().reshape(-1)
    
    return result

class ViterbiDecoder:

    def __init__(self, G):
        self.G = G                        # generator matrix
        self.r, self.K = G.shape
        self.nstates = 2**(self.K-1)           # number of states
        self.states = range(self.nstates) # the states themselves

        # States are kept as integers, not binary strings or arrays.
        # For instance, the state "10" would be kept as "2", "11" as
        # 3, etc.

        # self.predecessor_states[s] = (s1, s2), where s1 and s2 are
        # the two predecessor states for state s (i.e., the two states
        # that have edges into s in the trellis).
        self.predecessor_states = [((2*s+0) % self.nstates, (2*s+1) % self.nstates) for s in self.states]

        # self.expected_parity[s1][s2] = the parity when transitioning
        # from s1 to s2 ('None' if there is no transition from s1 to
        # s2).  This is set up as a dictionary in init, for
        # efficiency.  For inefficiency, you could call
        # calculate_expected_parity() each time.
        self.expected_parity = defaultdict(lambda:defaultdict(float))
        for (s1, s2) in [(s1, s2) for s1 in self.states for s2 in self.states]:
            self.expected_parity[s1][s2] = self.calculate_expected_parity(s1, s2) if s1 in self.predecessor_states[s2] else None

    # Converts integers to bit arrays.  This method may or may not be
    # useful to you; it depends on your particular implementation.
    @staticmethod
    def int_to_bit_array(i, length):
        return numpy.array([int(q) for q in (length-len(bin(i)))*'0'+bin(i)[2:]])

    def calculate_expected_parity(self, from_state, to_state):

        # x[n] comes from to_state
        # x[n-1] ... x[n-k-1] comes from from_state
        x = ((to_state >> (self.K-2)) << (self.K-1)) + from_state

        # Turn the state integer into an array of bits, so that we can
        # xor (essentially) with G
        z = ViterbiDecoder.int_to_bit_array(x, self.K+2)
        return self.G.dot(z) % 2

    def branch_metric(self, expected, received, soft_decoding=False):
        metric=0
        if not soft_decoding:
            #print "Hey! I am the hardcore"
            digitized=[]
           
            for volt in received:
                if volt>.5:
                    volt=1
                    #print (volt, 
                    digitized.append(volt)
                else:
                    volt=0
                    digitized.append(volt)
            for i in range(len(received.tolist())):
                if digitized[i]!=expected[i]:
                    #print (digitized[i], expected[i])
                    metric+=1
            #print received, expected
        else:
            for i in range(len(received.tolist())):
                metric=metric+(expected[i]-received[i])**2
            #print "Hey! I am soft!"
        return metric 

    def viterbi_step(self, n, received_voltages):
        for s in self.states:
            pred=self.predecessor_states[s]
            #print pred
            bm1=self.branch_metric(self.calculate_expected_parity(pred[0],s), received_voltages)
            #print self.calculate_expected_parity(pred[0],s), self.calculate_expected_parity(pred[1],s)
            #print (pred[0],s),self.calculate_expected_parity(pred[0],s)
            #print (pred[1],s),self.calculate_expected_parity(pred[1],s)
            #print bm1
            bm2=self.branch_metric(self.calculate_expected_parity(pred[1],s), received_voltages)
            pm1=bm1+self.PM[pred[0],n-1]
            #print pm1
            pm2=bm2+self.PM[pred[1],n-1]
            #print pm2
            if pm1<pm2:
                self.Predecessor[s,n]=pred[0]
                self.PM[s,n]=pm1
                
            else:
                self.Predecessor[s,n]=pred[1]
                self.PM[s,n]=pm2

    def most_likely_state(self, n):
        pm_state_dict={self.PM[state,n]: state for state in self.states}
        smallest_pm=min(pm_state_dict.keys())
        most_likely=pm_state_dict[smallest_pm]
        return most_likely

    def traceback(self,s,n):
        # TODO: Your code here
        message=[]
        state=s
        path=[s]
        for i in range(n):
            time=n-i
            p=self.Predecessor[state,time]
            if p<state:
                bit=1
                message.append(bit)
                state=p
                path.append(p)
            elif p>state:
                bit=0
                message.append(bit)
                state=p
                path.append(p)
            else:
                if p==0:
                    bit=0
                    message.append(bit)
                    state=p
                    path.append(p)
                else:
                    bit=1
                    message.append(bit)
                    state=p
                    path.append(p)
        #print path
        return message[::-1]           
                               
        

    # The main decoding loop
    def decode(self, received_voltages):

        max_n = (len(received_voltages)/self.r) + 1

        # self.PM is the trellis itself; rows are states, columns are
        # time.  self.PM[s,n] is the metric for the most-likely path
        # through the trellis arriving at state s at time n.
        self.PM = numpy.zeros((self.nstates, max_n))

        # at time 0, the starting state is the most likely, the other
        # states are "infinitely" worse.
        self.PM[1:self.nstates,0] = 1000000

        # self.Predecessor[s,n] = predecessor state for s at time n.
        self.Predecessor = numpy.zeros((self.nstates,max_n), dtype=numpy.int)

        # Viterbi Algorithm:
        n = 0
        for i in range(0, len(received_voltages), self.r):
            n += 1
            # Fill in the next columns of PM, Predecessor based
            # on info in the next r incoming parity bits
            self.viterbi_step(n, received_voltages[i:i+self.r])

        # Find the most-likely ending state, and traceback to
        # reconstruct the message.
        s = self.most_likely_state(n)
        return self.traceback(s,n)

def test():
    m=numpy.asarray(list('0111011010')).astype(int)
    G = [[1, 1, 1], [1, 0, 1],[0,1,1]]
    #G=[[1,1,0],[1,1,1]]
    G=numpy.asarray(G)
    encoded=convolutional_encode(m, G)
    v=ViterbiDecoder(G)
    print v.calculate_expected_parity(1, 0)
    decoded=v.decode(encoded)
    return encoded, decoded
