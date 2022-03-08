import sys

keyFileName = sys.argv[1]
messageFileName = sys.argv[2]
cipherFileName = sys.argv[3]

keyFile = open(keyFileName, 'wb')
k = keyFile.read()
keyFile.close()
messageFile = open(messageFileName, 'r')
message = messageFile.read()
messageFile.close()

M = message.encode()
c = bytearray(len(M))
for i in range(len(M)):
   c[i] = k[i]^M[i]