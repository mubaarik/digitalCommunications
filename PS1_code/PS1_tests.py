from PS1 import huffman

def test_huffman_internal(symbols, expected_sizes):

    codebook = huffman(symbols)

    # Check for prefix-free-ness
    codes = codebook.values()
    for i, j in [(i, j) for i in range(len(codes)) for j in range(len(codes)) if i != j]:
        assert not codes[j].startswith(codes[i]),\
            "Code %s is a prefix of code %s" % (codes[i],codes[j])

    # Check expected sizes of encodings
    for symbol, expected in expected_sizes:
        got = len(codebook[symbol])
        assert (got == expected),\
               "For symbol %s: expected size %d, got %d" % (symbol,expected,got)

    print "-----------"
    for symbol, probability in symbols:
        print symbol, probability, codebook[symbol]


if __name__ == "__main__":
    # test case 1: four symbols with equal probability
    symbols = [("a", .25), ("b", .25), ("c", .25), ("d", .25)]
    expected = [("a", 2), ("b", 2), ("c", 2), ("d", 2)]
    test_huffman_internal(symbols, expected)

    # test case 2: example from section 22.3 in notes
    symbols = [("a", .34), ("b", .5), ("c", .08), ("d", .08)]
    expected = [("a", 2), ("b", 1), ("c", 3), ("d", 3)]
    test_huffman_internal(symbols, expected)

    # test case 3: example from Exercise 5 in notes
    symbols = [("I", .07), ("II", .23), ("III", .07), ("VI", .38), ("X", .13), ("XVI", .12)]
    expected = [("I", 4), ("II", 3), ("III", 4), ("VI", 1), ("X", 3), ("XVI", 3)]
    test_huffman_internal(symbols, expected)

    # test case 4: 3 flips of unfair coin
    phead = 0.9
    plist = []
    for flip1 in ('H','T'):
        p1 = phead if flip1 == 'H' else 1-phead
        for flip2 in ('H','T'):
            p2 = phead if flip2 == 'H' else 1-phead
            for flip3 in ('H','T'):
                p3 = phead if flip3 == 'H' else 1-phead
                plist.append((flip1+flip2+flip3, p1*p2*p3))
    expected_sizes = (("HHH", 1),("HTH", 3),("TTT",5))
    test_huffman_internal(plist, expected_sizes)
