import matplotlib.pyplot as plt
import re
import sys
import argparse

import config
import sendrecv
import sink

try:
    import PS1
except:
    print "Error: PS1.py does not exist.  Huffman encoding won't work."

class Transceiver:

    def __init__(self):
        self.tx_bits = None
        self.rx_bits = None
        self.encode_function = None
        self.decode_function = None
        self.options = config.PS0_Options()

    def set_debug_options(self, i, q, p, r):
        self.options.chunksize = i
        self.options.silence = q
        self.options.prefill = p
        self.options.samplerate = r

    '''
    Set the encoding type for this Transceiver
    '''
    def set_encode(self, t):

        if t == "huffman":
            self.encode_function = self.huffman_encode
            self.decode_function = self.huffman_decode
        elif t == "ascii":
            self.encode_function = Transceiver.ascii_encode
            self.decode_function = Transceiver.ascii_decode
        elif t == "five":
            self.encode_function = Transceiver.five_bit_encode
            self.decode_function = Transceiver.five_bit_decode
        else:
            print "Unknown encoding; using ASCII"
            self.encode_function = Transceiver.ascii_encode
            self.decode_function = Transceiver.ascii_decode

    def encode_string(self, tx_string):
        if tx_string is None:
            print "No string to encode"
            return
        self.tx_bits = self.encode_function(tx_string)
        return self.tx_bits

    def huffman_encode(self, string):
        symbols = PS1.get_probabilities(string)
        self.tree = PS1.huffman(symbols)
        encoded_string = PS1.huffman_encode(string)
        return [int(i) for i in encoded_string]

    def huffman_decode(self, bits):
        return PS1.huffman_decode(bits, self.tree)

    @staticmethod
    def ascii_encode(string):
        bits = []
        for c in string:
            bits.extend([ord(c) >> i & 1 for i in range(7, -1, -1)])
        return bits

    @staticmethod
    def ascii_decode(bits):
        string = ""
        try:
            for i in range(0, len(bits), 8):
                n = 0x00
                for j in range(8):
                    bit = bits[i+(7-j)]
                    n |= (bit << j)
                string += chr(n)
        except:
            print "Error decoding"
        return string

    @staticmethod
    def five_bit_encode(string):
        caps = re.compile("^([A-Z]| )+$")
        if not caps.match(string):
            print "String does not meet requirements for 5-bit encoding; must be entirely capital letters or spaces"
            sys.exit(-1)

        codebook = {chr(c) : c - ord("A") for c in range(ord("A"), ord("Z") + 1)}
        codebook[" "] = 26
        bits = []
        for c in string:
            n = codebook[c]
            bits.extend([n >> i & 1 for i in range(4, -1, -1)])
        return bits

    @staticmethod
    def five_bit_decode(bits):
        string = ""
        try:
            codebook = {c - ord("A") : chr(c) for c in range(ord("A"), ord("Z") + 1)}
            codebook[26] = " "
            for i in range(0, len(bits), 5):
                n = 0x00
                for j in range(5):
                    bit = bits[i+(4-j)]
                    n |= (bit << j)
                string += codebook[n]
        except:
            print "Error decoding"
        return string

    def set_spb(self, spb):
        self.options.spb = spb

    def set_carrier_frequency(self, fc):
        self.options.channel = [fc]

    def create_waveform(self, bits):
        # Sendrecv takes care of the modulation for us.  Normally we
        # wouldn't care very much about the un-modulated samples once
        # we had modulated them, but for this lab we need both to make
        # some graphs.
        c = sendrecv.get_waveform(self.options, bits)
        self.c = c
        samples = c.xmit_samples
        modulated_samples = c.mod_samples
        return samples, modulated_samples

    '''
    Send the message
    '''
    def send(self, waveform):
        # As with modulation, sendrecv takes care of the demodulation
        # for us (you'll learn how in a few weeks!). And again,
        # normally we wouldn't care very much about the received
        # waveform if we already had the demodulated samples, but
        # again, today we're making graphs.
        self.rx_bits = sendrecv.send_waveform(self.c, waveform)
        recv_waveform = self.c.recv_waveform
        demod_waveform = self.c.demod_samples
        return recv_waveform, demod_waveform
        
    def decode(self):
        if self.rx_bits is None:
            print "No bits to decode"
            return None
        print "Decoding %d bits" % len(self.rx_bits)
        return self.decode_function(self.rx_bits)

if __name__ == "__main__":

    # This code sets up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=int, help='lowest carrier frequency (Hz)', default=1000)
    parser.add_argument('-s', type=int, help='samples per bit', default=256)
    parser.add_argument('encoding', type=str, help='encoding type: ascii, five, or huffman', choices=['ascii', 'five', 'huffman'])

    # (These options are only useful for debugging.  If everything's
    # going well, you won't need them.)
    parser.add_argument('-i', type=int, help='samples per chunk (transmitter)', default=256)
    parser.add_argument("-q", type=int, default=80, help="#samples of silence at start of preamble")
    parser.add_argument("-p", type=int, default=60, help="write buffer prefill (transmitter)")
    parser.add_argument("-r", type=int, default=48000, help="sample rate (Hz)")
    args = parser.parse_args()

    print "Encoding type:", args.encoding
    print "Samples per bit:", args.s
    print "Carrier frequency:", args.c

    # This is the message we'll be sending.  Feel free to change it!
    text_to_transmit = "THIS CLASS IS THE BEST"
    t = Transceiver()
    t.set_debug_options(args.i, args.q, args.p, args.r)
    
    # 1. Convert the message to bits

    # Set the encoding type.  We have given you two: ASCII ('ascii'), and a 5-bit fixed-length encoding ('fixed').
    t.set_encode(args.encoding)
    encoded_bits = t.encode_string(text_to_transmit)
    print "Sending %d bits" % len(encoded_bits)

    # 2. Convert the message to a waveform

    # Set the number of samples per bit and the carrier frequency
    t.set_spb(args.s)               # Default: 256.  Try other values; powers of 2 are nice
    t.set_carrier_frequency(args.c) # Default: 1000.  Try other values; this one is fun to change
    unmod_samples, waveform = t.create_waveform(encoded_bits)
    print "Sending %d samples" % len(waveform)

    # 3. Send and receive the message

    # This sends the message and decodes it.  Much of this process is
    # abstracted away for now; we'll be learning more about it later
    # in the semester!
    recv_waveform, demod_samples = t.send(waveform)
    decoded_message = t.decode()
    print "Decoded message:", decoded_message

    # Some statistics: BPS, BER
    _, err = sink.hamming(encoded_bits, t.rx_bits)
    num_data_samples = len(encoded_bits) * t.options.spb
    total_time = num_data_samples / float(t.options.samplerate)
    bps = len(encoded_bits) / total_time
    print "Number of data bits per second:", bps
    print "Bit error rate:", err

    # 4. Fancy output.  Students need not be too concerned with this
    #    code :)

    # And some graphs
    plt.figure(1, figsize=(12,7))
    plt.subplot(221)
    plt.title("Unmodulated Samples")
    plt.ylim(-.5, 1.5)
    plt.xlim(0, len(encoded_bits) * t.options.spb)
    unmod_samples = unmod_samples[t.c.data_start:]

    bits = [i*1.2 - .1 for i in encoded_bits]
    bit_x = [i*t.options.spb + (t.options.spb/2.0) for i in range(len(bits))]

    plt.plot(range(len(unmod_samples)), unmod_samples)
    plt.plot(bit_x, bits, 'r.')

    plt.subplot(223)
    plt.title("Transmitted Waveform (zoom in!)")
    plt.ylim(-1.5, 1.5)
    plt.xlim(0, len(encoded_bits) * t.options.spb)
    waveform = waveform[t.c.data_start:]
    plt.plot(range(len(waveform)), waveform)

    plt.subplot(224)
    plt.title("Received Waveform (zoom in!)")
    plt.xlim(0, len(encoded_bits) * t.options.spb)
    recv_waveform = recv_waveform[t.c.recv_data_start + (24 + 16)*t.options.spb:]
    plt.plot(range(len(recv_waveform)), recv_waveform)

    plt.subplot(222)
    plt.title("Demodulated Waveform (zoom in!)")
    plt.xlim(0, len(encoded_bits) * t.options.spb)
    demod_samples = demod_samples[(24 + 16)*t.options.spb:]
    plt.plot(range(len(demod_samples)), demod_samples)

    plt.show()
