#!/usr/bin/env python3
import sys


text = sys.argv[1]


def cipherText(text):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    #Takes in a command line argument
    #creates a for loop for the key (range 0-25)
    for key in range(len(alpha)):
        plainText = ""
        #print(key)
    #Caesar Shifts
        for char in text:
            if char in alpha:
                plainText += plainText + chr((ord(char)+key-65)%26+65)
            print("k = " + str(key) + ": " + plainText + "\n" )
    #Prints out the key and the plaintext each time
    
cipherText(text)