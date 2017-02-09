import numpy
import random
import sys

import PS2

def insert_errors(bitstring, codeword_length, max_errors_per_codeword):
    # Convert the bitstring to an integer array so we can flip bits
    integer_bits = [int(i) for i in bitstring]
    # Move through codeword-by-codeword
    for i in range(0, len(bitstring), codeword_length):
        # Insert between 0 and max_errors_per_codeword errors into this word
        num_errors = random.randint(0, max_errors_per_codeword)
        # Randomize the bit indices in this codeword, and flip the
        # first num_errors of them (this is equivalent to randomly
        # selecting num_errors indeces without replacement)
        bit_indeces = range(i, i+codeword_length)
        random.shuffle(bit_indeces)
        for j in range(num_errors):
            ix = bit_indeces[j] # ix is the index of the bit to flip
            integer_bits[ix] = 1 - integer_bits[ix] # flip it

    # Note: If you'd like to figure out which bits were flipped, you
    # can keep track of the various values for ix, and print that at
    # the end.

    # Convert the integer array back to a string
    return "".join([str(b) for b in integer_bits])

def test_G():
    # Example 1 from page 67
    A = numpy.array([[1, 0, 1, 0, 0],
                     [1, 0, 0, 1, 0],
                     [1, 0, 0, 0, 1],
                     [0, 1, 1, 0, 0],
                     [0, 1, 0, 1, 0],
                     [0, 1, 0, 0, 1]])
    try:
        G = PS2.compute_G(A)
    except AttributeError:
        print "compute_G() is unimplemented -- not testing"
        return True
    if G is None:
        print "compute_G() is unimplemented -- not testing"
        return True
    if not isinstance(G, numpy.ndarray):
        print "compute_G() returns type other than numpy.ndarray -- not testing"
        # If you want to inspect your output visually, print G and compare to correct_G
        return True
    correct_G = numpy.array([[1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
                             [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                             [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                             [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
                             [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
                             [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1]])
    if not numpy.array_equal(G, correct_G):
        print "G matrix is incorrect"
        print "A:\n", A, "\nYour G:\n", G, "\nCorrect G:\n", correct_G
        return False
    
    # Example 2 from page 67
    A = numpy.array([[1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]])
    G = PS2.compute_G(A)
    correct_G = numpy.array([[1, 0, 0, 0, 1, 1, 0],
                             [0, 1, 0, 0, 1, 0, 1],
                             [0, 0, 1, 0, 0, 1, 1],
                             [0, 0, 0, 1, 1, 1, 1]])
    if not numpy.array_equal(G, correct_G):
        print "G matrix is incorrect"
        print "A:\n", A, "\nYour G:\n", G, "\nCorrect G:\n", correct_G
        return False
    return True


def test_encode():
    message_bits = "011011111010000001100101101111100000"
    # Example 1 from page 67
    A = numpy.array([[1, 0, 1, 0, 0], [1, 0, 0, 1, 0], [1, 0, 0, 0, 1], [0, 1, 1, 0, 0], [0, 1, 0, 1, 0], [0, 1, 0, 0, 1]])
    x = PS2.encode(A, message_bits)
    encoded_bits = "011011000001110101110100000101001100101100011011110101010000010100"

    if not isinstance(x, str):
        print "encode() should return", type(""), "not", type(x)
        return False
    if (x != encoded_bits):
        print "Encode incorrect\nA:\n", A, "\nMessage bits:\n", message_bits, "\nYour encoding:\n", x, "\nCorrect encoding:\n", encoded_bits
        return False

    # Example 2 from page 67
    A = numpy.array([[1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]])
    x = PS2.encode(A, message_bits)
    encoded_bits = "011011011111111010101000000001101100101010101101011100000000000"

    if not isinstance(x, str):
        print "encode() should return", type(""), "not", type(x)
        return False
    if (x != encoded_bits):
        print "Encode incorrect\nA:\n", A, "\nMessage bits:\n", message_bits, "\nYour encoding:\n", x, "\nCorrect encoding:\n", encoded_bits
        return False
    return True


def test_H():
    # Example 1 from page 71
    A = numpy.array([[1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]])
    try:
        H = PS2.compute_H(A)
    except AttributeError:
        print "compute_H() is unimplemented -- not testing"
        return True
    if H is None:
        print "compute_H() is unimplemented -- not testing"
        return True
    if not isinstance(H, numpy.ndarray):
        print "compute_H() returns type other than numpy.ndarray -- not testing"
        # If you want to inspect your output visually, print H and compare to correct_H
        return True
    correct_H = numpy.array([[1, 1, 0, 1, 1, 0, 0],
                             [1, 0, 1, 1, 0, 1, 0],
                             [0, 1, 1, 1, 0, 0, 1]])
    if not numpy.array_equal(H, correct_H):
        print "H matrix is incorrect"
        print "A:\n", A, "\nYour H:\n", H, "\nCorrect H:\n", correct_H
        return False
    return True

def test_decode(errors=False):

    message_bits = "011011111010000001100101101111100000"
    # Example 1 from page 67
    A = numpy.array([[1, 0, 1, 0, 0], [1, 0, 0, 1, 0], [1, 0, 0, 0, 1], [0, 1, 1, 0, 0], [0, 1, 0, 1, 0], [0, 1, 0, 0, 1]])
    encoded_bits = "011011000001110101110100000101001100101100011011110101010000010100"

    # Insert random errors
    if errors:
        (k, m) = A.shape
        encoded_bits = insert_errors(encoded_bits, k + m, 1)
    x = PS2.decode(A, encoded_bits)

    if not isinstance(x, str):
        print "decode() should return", type(""), "not", type(x)
        return False
    if (x != message_bits):
        print "Decode incorrect\nA:\n", A, "\nEncoded bits:\n", encoded_bits, "\nYour decoding:\n", x, "\nCorrect decoding:\n", message_bits
        return False

    # Example 2 from page 67
    A = numpy.array([[1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]])
    encoded_bits = "011011011111111010101000000001101100101010101101011100000000000"
    # Insert random errors
    if errors:
        (k, m) = A.shape
        encoded_bits = insert_errors(encoded_bits, k+m, 1)

    x = PS2.decode(A, encoded_bits)

    if not isinstance(x, str):
        print "encode() should return", type(""), "not", type(x)
        return False
    if (x != message_bits):
        print "Decode incorrect\nA:\n", A, "\nEncoded bits:\n", encoded_bits, "\nYour decoding:\n", x, "\nCorrect decoding:\n", message_bits
        return False
    return True
    

def run_all_tests(encode, decode):
    # If you don't want to run a particular test, just comment out the
    # appropriate lines.
    if encode:
        x = test_G()
        if not x: return
        x = test_encode()
        if not x: return
    if decode:
        x = test_H()
        if not x: return
        x = test_decode()
        if not x: return
        for i in range(100):
            x = test_decode(errors=True)
            if not x: return
    print "All tests passed"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        run_all_tests(True, True)
    elif sys.argv[1] == "encode":
        run_all_tests(True, False)
    elif sys.argv[1] == "decode":
        run_all_tests(False, True)
    else:
        run_all_tests(True, True)
