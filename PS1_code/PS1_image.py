import sys
import numpy
import matplotlib.pyplot as plt
from collections import defaultdict

def get_bits_from_byte(byte):
    bits = [0] * 8
    for i in range(8):
        bits[7-i] = (byte >> i) & 1
        assert(bits[i] == 0 or bits[i] == 1)
    return bits

def get_bits_from_bitmap(filename):

    img = plt.imread(filename)

    # Grey-scale image
    if len(img.shape) == 2:
        nrows, ncols = img.shape
        y = numpy.reshape(img,-1)
    else:
        nrows, ncols, pixel = img.shape
        # RGB image
        if pixel == 3:
            rgb2y = numpy.array([[.299],[.587],[.114]])
            x = numpy.reshape(img,(-1,3))
        # RGBA image
        elif pixel == 4:
            rgb2y = numpy.array([[.299],[.587],[.114],[0]])
            x = numpy.reshape(img,(-1,4))
        y = numpy.reshape(numpy.dot(x,rgb2y),-1)

    # Convert to black/white pixels
    bw = (numpy.reshape(y,-1) >= .5) * 1
    return bw

def get_run_probabilities(runs):
    run_dict = defaultdict(int)
    for run in runs:
        run_dict[run] += 1
    for run in run_dict:
        run_dict[run] /= float(len(runs))
    run_probs = [(run_length, run_dict[run_length]) for run_length in run_dict]
    run_probs.sort(key=lambda x: x[1], reverse=True)
    return run_probs

def get_run_lengths(filename, fixed_length=False):
    bits = get_bits_from_bitmap(filename)
    run_lengths = []
    current_bit = 1
    current_run_length = 0
    for bit in bits:
        if bit == current_bit:
            if fixed_length and current_run_length == 255:
                run_lengths.append(current_run_length)
                run_lengths.append(0)
                current_run_length = 0
            current_run_length += 1
        else:
            run_lengths.append(current_run_length)
            current_bit = 0 if current_bit == 1 else 1
            current_run_length = 1
    run_lengths.append(current_run_length)
    return run_lengths

def get_image_blocks(filename, width=500, height=500):
    assert (width % 4 == 0 and height % 4 == 0)
    bits = get_bits_from_bitmap(filename)
    k = bits.reshape((500,500))
    bits = []
    for row_index in range(0, height, 4):
        for col_index in range(0, width, 4):
            block = numpy.concatenate([k[row_index + i][col_index:col_index+4] for i in range(4)])
            n = 0x0000
            for i in range(len(block)):
                bit = block[15 - i]
                n |= (bit << i)
            assert (n <= 0xFFFF)
            bits.append(n)
    assert (len(bits) == width*height/16)
    return bits
