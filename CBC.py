import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import sys

'''======================================================================
to do: choose a random key
output: bytes type; 16 bytes
======================================================================'''
def gen():
    randomKey = os.urandom(16)
    return(randomKey)

'''======================================================================
to do: add a padding to ensure the length of the padded data is
        a multiple of 16
input: bytes type
output: bytes type.
WARNING: CAREFULLY READ THE NOTES and figure out what to do
======================================================================'''
def add_padding(data):
    msg = data
    if len(data) % 16 == 0:
        paddedMsg = bytearray()
        for i in range(16):
            paddedMsg.append(16)
        return(data + paddedMsg)
    else:
        padLen = 16 - len(msg) % 16
        paddedMsg = bytearray()
        for i in range(padLen):
            paddedMsg.append(padLen)
        msg += paddedMsg
        return(msg)
'''======================================================================
to do: remove the padding and return the original data before padding.
       do the reverse of add_padding
    1. see if the length of the input data is a mutiple of 16
    2. see if the padding is correct IN EVERY BYTE of the padding
    3. if everything is good, then take out the padding
input: bytes type
output: m, b
    m: bytes type.
    b: True/False.
======================================================================'''
def remove_padding(data):
    padNum = 0
    msg = data
    returnTrue = bytearray(msg)
    returnFalse = bytearray()
    if len(msg) % 16 == 0:
        i = len(msg) - 16
        while i < (len(msg)):
            if msg[i] in range(0, 17):
                if msg[i] == msg[i + 1]:
                    padNum = len(msg) - msg[i]
                    returnTrue = returnTrue[0:padNum]
                    return(returnTrue, True)
                else:
                    return(returnFalse, False)
            i += 1
    else:
        return(returnFalse, False)

'''======================================================================
to do: implement CBC encryption.
    1. Create AES object aes using AES.new
       You should give (key, mode, iv) CORRECTLY when you call AES.new
    2. Call add_padding you implemented above to pad the message m
    3. Call aes.encrypt by giving the padded message as an argument
input:
    k: bytes type, must be 16 bytes
    iv: bytes type, must be 16 bytes
    m: bytes type, any arbitrary-length message.
output:
    bytes: ciphertext encrypted with CBC mode
======================================================================'''
def encrypt_basic(k, iv, m):
    #iv = os.urandom(16)
    #k = gen()
    aes = AES.new(k, AES.MODE_CBC, iv)
    paddedMsg = add_padding(m)
    ciphertext = aes.encrypt(paddedMsg)
    return(ciphertext)

'''======================================================================
to do: implement CBC decryption.
    1. Create AES object aes using AES.new
       You should give (key, iv, mode) CORRECTLY when you call AES.new
    2. Call aes.decrypt on the given ciphertext
    3. Call remove_padding you implemented above to extract the original message m
input:
    k: bytes type, must be 16 bytes
    iv: bytes type, must be 16 bytes
    c: bytes type, any arbitrary-length ciphertext.
output: m
    m: bytes type - plaintext decrypted with CBC mode
        return an empty bytes object if an error occurs
======================================================================'''
def decrypt_basic(k, iv, c):
    aes = AES.new(k, AES.MODE_CBC, iv)
    plainText = bytearray(aes.decrypt(c))
    unpad, bol = remove_padding(plainText)
    return bytes(unpad)
'''======================================================================
to do: implement full CBC encryption.
    1. Generate a random iv (16 bytes)
    2. call encrypt_basic and get the ciphertext c0
    3. return the full ciphetext: iv + c0
input:
    k: bytes type, must be 16 bytes
    m: bytes type, any arbitrary-length message.
output:
    bytes type: ciphertext encrypted with CBC mode
======================================================================'''
def encrypt(k, m):
    iv = os.urandom(16)
    c = encrypt_basic(k, iv, m)
    c = iv + c
    return(c)


'''======================================================================
to do: implement full CBC decryption.
    1. Given c, extract iv and the rest c0
    2. call decrypt_basic to decrypt c0
input:
    k: bytes type, must be 16 bytes
    c: bytes type, any arbitrary-length ciphertext.
        Remember the full ciphertext c is really iv + c0
output: m
    m: bytes type - plaintext decrypted with CBC mode
        return an empty bytes object if an error occurs
======================================================================'''
def decrypt(k, c):
    iv = os.urandom(16)
    m = decrypt_basic(k, iv, c)
    m = iv - c
    return(m)





