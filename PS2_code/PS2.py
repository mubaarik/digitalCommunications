import numpy
def compute_G(A):
    # This method is OPTIONAL.  If implemented, it should take the A
    # matrix (a numpy.ndarray) and return the appropriate G matrix
    # (also a numpy.ndarray).  If you choose to use this method, you
    # will call it as part of encode().
    l=len(A)
    g=numpy.concatenate((numpy.identity(l), A), axis=1)
    G=g.astype(int)           
        
    return G

def compute_H(A):
    # This method is OPTIONAL.  If implemented, it should take the A
    # matrix (a numpy.ndarray) and return the appropriate H matrix
    # (also a numpy.ndarray).  IF you choose to use this method, you
    # will call it as part of decode().
    
    try:
        l=len(A[0])
        h=numpy.concatenate((numpy.asarray(A).T, numpy.identity(l)), axis=1)
        H=h.astype(int)
        
    except Exception, e:
        H=[]
        print str(e)
    return H

def compute_syndromes(H):
    # This method is OPTIONAL.  If implemented, it should take the H
    # matrix (a numpy.ndarray) and return a dictionary that provides a
    # mapping between error vectors and their corresponding symbols.
    # The data structures used within the mapping will differ
    # depending on your implementation of decode; for this reason, we
    # do not provide an explicit testing method for this function.  If
    # you choose to use this method, you will call it as part of
    # decode().
    dictionary={}
    try:
        H=H.astype(int)
        cols=len(H[0])
        rows=len(H)
        error_vectors=numpy.identity(cols).astype(int)
        for i in range(cols):
            error_vector=error_vectors[i]
            sydrome=numpy.asarray(H).dot(error_vector.T)
            dictionary[''.join(str(x) for x in sydrome.tolist())]=''.join(str(x) for x in error_vector.tolist())
    except Exception, e:
        print str(e)
    return dictionary
def block_k(k, y):
    blocks=[]
    a=k
    k0=0
    while a<len(y):
        blocks.append(y[k0:a])
        k0=a
        a=a+k
    if len(y[k0:])>0:
        blocks.append(y[k0:])
    return blocks
def encode(A, message):
    
    # This method is REQUIRED.  Here, you should implement the linear
    # encoder.  This requires the following steps:
    # 1. Calculate the G matrix
    # 2. Break the message into k-length blocks
    # 3. Use G to determine the codewords for each block
    # 4. Concatenate the codewords into a single string and return it
    G=compute_G(A)
    k=len(A)
    blocks=block_k(k, message)
    codewords=''
    for block in blocks[0:-1]:
        block=numpy.asarray(list(block)).astype(int)
        codeword=block.dot(G)%2
        codeword=''.join((codeword.astype(str)).tolist())
        codewords=codewords+codeword
    if len(blocks[-1])<k:
        extra_zeroes='0'*(k-len(blocks[-1]))
        end_block=blocks[-1]+extra_zeroes
        end_block=numpy.asarray(list(end_block)).astype(int)
        
        codeword=end_block.dot(G)
       
        codeword=end_block.dot(G)%2
        
        #print codeword
        #print blocks[-1]
        #print codeword[0:len(blocks[-1])], codeword[(k):]
        codeword=numpy.concatenate((numpy.asarray(codeword[0:len(blocks[-1])]), numpy.asarray(codeword[(k):])), axis=1)
        #print codeword
        codeword=''.join((codeword.astype(str)).tolist())
        codewords=codewords+codeword
    else:
        block=blocks[-1]
        block=numpy.asarray(list(block)).astype(int)
        codeword=block.dot(G)%2
        codeword=''.join((codeword.astype(str)).tolist())
        codewords=codewords+codeword
    return codewords
                         
                         
    

def decode(A, encoded_bits):
    # This method is REQUIRED.  Here you should implement the syndrome
    # decoder.  This requires the following steps:
    # 1. Calculate the H matrix
    # 2. Use H to set up the syndrome table
    # 3. Break the message into n-length codewords
    # 4. For each codeword, calculate the error bits
    # 5. If the error bits are nonzero, use the syndrome table to correct the error.
    # 6. Return the corrected bitstring
    #
    # Though we are not requiring it, we recommend you set up the
    # syndrome table before you perform the decoding, via the
    # compute_syndromes() function.  This will result in a more
    # organized design, and also a more efficient decoding procedure
    # (because you won't be recalculating the syndrome table for each
    # codeword).
    H=compute_H(A)
    n=len(H[0])
    k=len(A)
    syndrome_length=len(A[0])
    #print syndrome_length
    blocks=''
    codewords=block_k(n, encoded_bits)
    syndromes=compute_syndromes(H)
    #print syndromes
    for codeword in codewords[0:-1]:
        codeword=numpy.asarray(list(codeword)).astype(int)
        syndrome=H.dot(codeword.T)%2
        #print ''.join((syndrome).astype(str).tolist())
        if syndrome.tolist()!=[0]*syndrome_length:
            syndrome=''.join((syndrome).astype(str).tolist())
            error_vector=numpy.asarray(list(syndromes[syndrome][0:k])).astype(int)
            block=(codeword[0:k]+error_vector)%2
            block=''.join((block).astype(str).tolist())
            blocks=blocks+block
        else:
            block=codeword[0:k]
            block=''.join((block).astype(str).tolist())
            blocks=blocks+block
    if len(codewords[-1])<n:
        codeword=codewords[-1]
        #print "codeword="+str(codeword)
        length=len(codeword)
        parity=codeword[(k-(n-length)):]
       # print "parity="+str(parity)
        word=codeword[0:(length-len(parity))]
       # print "word="+str(word)
        word=word+'0'*(n-length)
        codeword=word+parity
        codeword=numpy.asarray(list(codeword)).astype(int)
        syndrome=H.dot(codeword.T)%2
        if syndrome.tolist()!=[0]*syndrome_length:
            syndrome=''.join((syndrome).astype(str).tolist())
            error_vector=numpy.asarray(list(syndromes[syndrome][0:k])).astype(int)
            block=(codeword[0:k]+error_vector)%2
            block=block[0:(length-len(parity))]
            block=''.join((block).astype(str).tolist())
            blocks=blocks+block
        else:
            block=codeword[0:k]
            block=block[0:(length-len(parity))]
            block=''.join((block).astype(str).tolist())
            blocks=blocks+block
    else:
        codeword=codewords[-1]
        codeword=numpy.asarray(list(codeword)).astype(int)
        syndrome=H.dot(codeword.T)%2
        if syndrome.tolist()!=[0]*syndrome_length:
            syndrome=''.join((syndrome).astype(str).tolist())
            error_vector=numpy.asarray(list(syndromes[syndrome][0:k])).astype(int)
            block=(codeword[0:k]+error_vector)%2
            block=''.join((block).astype(str).tolist())
            blocks=blocks+block
        else:
            block=codeword[0:k]
            block=''.join((block).astype(str).tolist())
            blocks=blocks+block
        
    return blocks
def encode_test():
    A=[[1,1,0,1],[1,0,1,1],[0,1,1,1]]
    A=numpy.asarray(A)
    A=A.T
    import random
    bit='101010'
    message=''
    for i in range(83):
        message=message+random.choice(bit)
    print "revieved messsage="+message
    encoded=encode(A, message)
    print "encoded="+encoded
    decoded=decode(A, encoded)
    print "decoded="+decoded
    for i in range(min(len(message), len(decoded))):
        if message[i]!=decoded[i]:
            print message[i], decoded[i]
    
    
