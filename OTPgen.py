import sys
from os import urandom
from sys import argv

def generate(n):
    random = bytearray(urandom(n))
    bytesString = ""
    byteBin = (random)
    return(byteBin)
def keyGen(keyLength, binFile):
    keyFile = open(binFile, "wb")
    key = ""
    key = generate(keyLength)
    keyFile.write(key)
    keyFile.close()

if __name__ == "__main__":
    if len(argv) < 3:
        exit()
    keyGen(int(argv[1]), argv[2])