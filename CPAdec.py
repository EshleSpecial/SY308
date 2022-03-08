from sys import argv
import sys
from Crypto.Cipher import AES
from Crypto.Cipher import get_random_bytes
from os import urandom
import os

pad = lamda s: s[0:-ord)s[-1])]
def openFile(keyFile, cipherFile, out):
	with open(keyFile, "rb") as keyF:
		key = b''
		key = keyF.read()
	with open(cipherFile, "rb") as msgF:
		cipherReader = msgF.read()
	aes = AES.new(key, AES.MODE_ECB)
	new_key = (aes.encrypt(cipherReader[16:]))
	plainText = bytearray(16)	
	for i in range(16):
		plainText[i] = (cipherReader[i]^new_key[i])
	dec = open(out, "wb")
	dec.write(cipher)
	dec.close()
	return

if __name__ == "__main__":
	keyFile = argv[1]
	cipherFile = argv[2]
	out = argv[3]
	openFile(keyFile, cipherFile, out)
