import heapq
import operator
import sys

from collections import defaultdict

class HuffmanTree:

    # Huffman Trees always have a probability.  For internal nodes,
    # symbol will be None, and left and right children will be
    # defined.  For leaf nodes, symbol will *not* be None, but the
    # children will be.
    def __init__(self, symbol, probability):
        self.left_child = None
        self.right_child = None
        self.probability = probability
        self.symbol = symbol

    # "less than" method, for sorting trees
    def __lt__(self, other):
        return self.probability < other.probability

    def codebook(self, current_bitstring=""):
        # If we're at a leaf, return our symbol
        if self.left_child == None:
            book = {}
            book[self.symbol] = current_bitstring
        # Else, walk down the tree.  Zeros on the left, ones on the right
        else:
            book = self.left_child.codebook(current_bitstring + "0")
            book1 = self.right_child.codebook(current_bitstring + "1")
            book.update(book1) # Merge the two dictionaries into one book
        return book
        
# Input:
#   symbols, a list of (symbol, probability) tuples
# Output:
#   codebook, which maps symbols to bitstrings
def huffman(symbols):

    # Probabilities need to sum to 1
    assert(sum([i for (_, i) in symbols]) >= .999999 and sum([i for (_, i) in symbols]) <= 1.000001)

    # Degenerate case: only one symbol to encode
    if len(symbols) == 1:
        return {symbols[0][0] : "0"}

    # Convert the list of symbols into a min-heap that sorts
    # HuffmanTrees instead of (symbol, probability) tuples
    min_heap = []
    for item in symbols:
        h = HuffmanTree(item[0], item[1])
        min_heap.append(h)
    heapq.heapify(min_heap)

    while len(min_heap) > 1:
        # Take the two smallest elements out
        a = heapq.heappop(min_heap)
        b = heapq.heappop(min_heap)

        # Create a new Huffman tree out of the two smallest elements
        c = HuffmanTree(None, a.probability + b.probability)
        c.left_child = a
        c.right_child = b
        heapq.heappush(min_heap, c)

    # Return the codebook
    return min_heap[0].codebook()


''' Calculate the probability of each symbol in data '''
def get_probabilities(data):
    # Count each element
    symbol_dict = defaultdict(int)
    for element in data:
        symbol_dict[element] += 1
    # Turn counts into probabilities
    symbols = []
    for element in symbol_dict:
        symbols.append((element, symbol_dict[element] / float(len(data))))
    assert(sum([i for (_, i) in symbols]) >= .999999 and sum([i for (_, i) in symbols]) <= 1.000001) # probabilities sum to 1
    return symbols


'''Huffman source-encoding; symbols are calculated directly from the
data if not otherwise given'''
def huffman_encode(data, symbols=None):
    if symbols is None:
        symbols = get_probabilities(data)
    codebook = huffman(symbols)
    s = ""
    for c in data:
        s += codebook[c]
    return s

'''Huffman decoding'''
def huffman_decode(bits, codebook):
    reverse_codebook = {codebook[c] : c for c in codebook}
    output = ""
    j = ""
    for i in bits:
        j += str(i)
        if j in reverse_codebook:
            output += reverse_codebook[j]
            j = ""
    return output

if __name__ == "__main__":

    import PS1_image
    filename = "PS1_fax_image.png"

    # 1. Individual bits
    bits = PS1_image.get_bits_from_bitmap(filename)
    num_bits = len(bits)
    print "Encoding 1: Individual bits"
    print "   %d bits" % num_bits
    
    # 2. Fixed-length runs
    runs = PS1_image.get_run_lengths(filename, fixed_length=True)
    if len(runs) % 2 != 0:
        runs.append(0)
    num_bits = len(runs) * 8
    print "Encoding 2: Fixed-length runs"
    print "   %d runs" % len(runs)
    print "   %d bits" % num_bits

    # 3. Huffman-encoded runs
    s = huffman_encode(runs)
    print "Encoding 3: Huffman-encoded runs\n   %d bits" % len(s)

    # Get the probability of each run length
    run_probs = PS1_image.get_run_probabilities(runs)
    print "   Top 10 run lengths [probability]:"
    for i in range(10):
        print "      %d [%2.2f]" % (run_probs[i][0], run_probs[i][1])
    
    # 4. Huffman-encoded runs, separate colors
    white_runs = [runs[i] for i in range(len(runs)) if i % 2 == 0]
    black_runs = [runs[i] for i in range(len(runs)) if i % 2 == 1]
    white_string = huffman_encode(white_runs)
    black_string = huffman_encode(black_runs)
    print "Encoding 4: Huffman-encoded runs by color\n   %d bits" % (len(white_string) + len(black_string))

    # Get the probabilities of the run lengths
    white_run_probs = PS1_image.get_run_probabilities(white_runs)
    print "   Top 10 white run lengths [probability]:"
    for i in range(10):
        print "      %d [%2.2f]" % (white_run_probs[i][0], white_run_probs[i][1])
    black_run_probs = PS1_image.get_run_probabilities(black_runs)
    print "   Top 10 black run lengths [probability]:"
    for i in range(10):
        print "      %d [%2.2f]" % (black_run_probs[i][0], black_run_probs[i][1])

    # 5. Huffman-encoded runs, allow pairs
    paired_runs = [(runs[i], runs[i+1]) for i in range(0, len(runs), 2)]
    s = huffman_encode(paired_runs)
    print "Encoding 5: Huffman-encoded run pairs\n   %d bits" % len(s)

    # Get the probabilities
    run_probs = PS1_image.get_run_probabilities(paired_runs)
    print "   Top 10 run lengths [probability]:"
    for i in range(10):
        print "      %s [%2.2f]" % (run_probs[i][0], run_probs[i][1])

    # 6. Huffman-encoded blocks
    blocks = PS1_image.get_image_blocks(filename)
    s = huffman_encode(blocks)
    print "Encoding 6: Huffman-encoded 4x4 image blocks\n   %d bits" % len(s)

    # Get the probabilities
    run_probs = PS1_image.get_run_probabilities(blocks)
    print "   Top 10 4x4 blocks [probability]:"
    for i in range(10):
        print "      %s [%2.2f]" % (hex(run_probs[i][0])[:-1], run_probs[i][1])

    # 7. Run-length encoding on a different image
    runs_v = PS1_image.get_run_lengths("PS1_voyager.png", fixed_length=True)
    if len(runs) % 2 != 0:
        runs_v.append(0)

    # For any run lengths that don't exist, we'll assume a probability
    # of zero.
    p = get_probabilities(runs)
    x = [i for (i, j) in p]
    for i in range(0, 256):
        if i not in x:
            p.append((i, 0.0))

    s = huffman_encode(runs_v, symbols=p)
    print "Final experiment: Huffman-encoded runs on a different image"
    print "   Using probabilities calculated from previous image: %d bits" % len(s)
    s = huffman_encode(runs_v)
    print "   Using probabilities calculated from source image: %d bits" % len(s)

