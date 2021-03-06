import argparse
import struct
import array

def ascii_dict():
    dictt={}
    ascii_chrs=[chr(i) for i in range(256)]
    for i in ascii_chrs:
        dictt[i]=ord(i)
    return dictt
def lzw_compress(filename, max_size=2**16):
    table=ascii_dict()
    out='Mubarik.zl'
    output=open(out, 'wb')#open output file for write
    mfile=open(filename, 'rb')#open input file for 
    data=mfile.read()
    length=len(data)
    string=data[0]#the start of my string 
    current=1#the end of my string
    largest=255
    while current<=(length-1):
        symbol=data[current]
        current+=1
        if string+symbol in table.keys():
#            print "if"
            string=string+symbol
        else:
#            print "else"
            new_word=string+symbol
            send=string
            string=symbol
            table[new_word]=largest+1
            largest=largest+1
            output.write(struct.pack('H',table[send]))
            if largest==max_size-1:
                print "else if"
                table=ascii_dict()
                largest=255
    send=string
    output.write(struct.pack('H',table[send]))
    output.close()
    mfile.close()
    print largest

            
def numbers_words():
    dic={}
    for i in range(256):
        dic[i]=chr(i)
    return dic
    

def lzw_decompress(filename, max_size=2**16):
    table=numbers_words()
    out='Mubarik.dat'
    output=open(out, 'w')
    inputFile=open(filename, 'rb')
    compressed=array.array('H', inputFile.read())
   # print compressed
    length=len(compressed)
    print length
    code=compressed[0]
    string=table[code]
    output.write(string)
    current=1
    largest=255
    while current<length:
        code=compressed[current]
        current+=1
        if code not in table.keys():
            entry=string+string[0]
        else:
            entry=table[code]
        output.write(entry)
        table[largest+1]=string+entry[0]
        largest=largest+1
        string=entry
        if largest==(max_size-1):
            table=numbers_words()
            largest=255
    inputFile.close()
    output.close()
    print largest
   #l parserss

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, help='filename to compress or decompress', default='test')
    parser.add_argument('-d', '--decompress', help='decompress file', action='store_true')

    args = parser.parse_args()

    if not args.decompress:
        lzw_compress(args.filename)
    else:
        lzw_decompress(args.filename)


