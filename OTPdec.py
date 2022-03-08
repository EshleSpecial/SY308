from sys import argv
import sys
from os import urandom

def decryption(keyFile, CipherFile, out):
    decryption = ""
    with open(keyFile, "rb") as kf:
        key = b""
        for i in kf:
            key += i
    with open(CipherFile, "rb") as cf:
        cipher = b""
        for c in cf:
            cipher += c

    if len(cipher) > len(key):
        print("Key must be same size as cipher")
        exit()
    denc = open(out, "wb")
    decryption = bytearray(len(cipher))
    for j in range(len(cipher)):
        decryption[j] = (key[j] ^ cipher[j])
    denc.write(decryption)
    denc.close()

if __name__ == "__main__":
    if len(argv) < 4:
        exit()
    decryption(argv[1], argv[2], argv[3])