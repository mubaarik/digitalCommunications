import numpy
import random
import sys
import PS3 as viterbi

def decode(voltages, G):
    decoder = viterbi.ViterbiDecoder(G)
    return decoder.decode(voltages)

def test_equality(sent, recv, voltages):
    if numpy.any(sent != recv):
        print "Test failed"
        print "Original message:", sent
        print "Sent voltages:", voltages
        print "Decoded message:", recv
        sys.exit(-1)

def test_1():
    G = numpy.array([[1, 1, 1], [1, 0, 1], [0, 1, 1]])
    print "Testing hard-decision decoding with no errors, G =", str(G.tolist())
    for i in range(100):
        message = numpy.random.random_integers(0, 1, 10)
        voltages = viterbi.convolutional_encode(message, G)
        decoded_message = decode(voltages, G)
        test_equality(message, decoded_message, voltages)

def test_2():
    G = numpy.array([[1, 1, 1], [1, 1, 0]])
    print "Testing hard-decision decoding with no errors, G =", str(G.tolist())
    for i in range(100):
        message = numpy.random.random_integers(0, 1, 10)
        voltages = viterbi.convolutional_encode(message, G)
        decoded_message = decode(voltages, G)
        test_equality(message, decoded_message, voltages)
    
def test_3():
    G = numpy.array([[1, 1, 1], [1, 1, 0]])
    print "Testing hard-decision decoding with errors, G =", str(G.tolist())
    for i in range(100):
        message = numpy.random.random_integers(0, 1, 10)
        voltages = viterbi.convolutional_encode(message, G)
        # Make sure the errors are spaced far apart, and not too close
        # to the end of the message.
        err1 = random.randint(0, 4)
        err2 = random.randint(11, 15)
        voltages[err1] = 1 - voltages[err1]
        voltages[err2] = 1 - voltages[err2]
        decoded_message = decode(voltages, G)
        test_equality(message, decoded_message, voltages)

def test_4():
    G = numpy.array([[1, 1, 1], [1, 1, 0]])
    print "Testing soft-decision decoding, G =", str(G.tolist())
    for i in range(10):
        expected = numpy.random.random_integers(0,1,len(G))
        received = numpy.random.rand(len(G))
        decoder = viterbi.ViterbiDecoder(G)
        dist = decoder.branch_metric(expected, received, soft_decoding=True)
        expected_dist = sum([(expected[j] - received[j])**2 for j in range(len(G))])
        if numpy.any((dist - expected_dist) > 1e-5):
            print "Soft branch_metric failed"
            print "Expected voltages:", expected
            print "Received voltages:", received
            print "Value returned by branch_metric:", dist
            print "Expected return value:",expected_dist
            sys.exit(-1)

if __name__ == "__main__":
    test_1() # Hard decision test 1
    test_2() # Hard decision test 2
    test_3() # Hard decision test 3 (with errors)
    test_4() # Uncomment this out to test soft-decision decoding
    print "All tests passed!  Whoo!"
