from sys import argv
import sys
from os import urandom

def encryption(keyFile, messageFile, out):
    cipher = ""
    with open(keyFile, "rb") as kf:
        key = b""
        for i in kf:
            key += i
    with open(messageFile, "rb") as mf:
        message = b""
        for m in mf:
            message += m

    if len(message) > len(key):
        print("Key must be same size as message")
        exit()
    enc = open(out, "wb")
    cipher = bytearray(len(message))
    for j in range(len(message)):
        cipher[j] = (key[j] ^ message[j])
    enc.write(cipher)
    enc.close()

if __name__ == "__main__":
    if len(argv) < 4:
        exit()
    encryption(argv[1], argv[2], argv[3])