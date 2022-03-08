#SY308 Intial Self Assessment
#MIDN McKenzie Eshleman
#221938
#19JAN21


#Problem 1
#Function that accepts two list of integers and returns
#a new list which is the compontent sum. 
def listSums(x,y):
    newList = []
    for i in x:
        for j in y:
            Sum = i + j
            newList.append(Sum)
    return newList


#Problem 2
#Accepts a single command line argument, a filename, and loops
#throught the lines in the file, printing each line only if it
#is a valid SCY course number,
#first 2 characters should be "SY"
#1) read a file from a command line
#2) read each individual line in the file
#3) Breaks apart the first two strings in each line
#4) Continue with the SY courses and printing

#REFERNECED MY PROJECT 1 FROM SY 301 TO SEE THE FILE OPENING TECHNIQUES
def scyFile(Filename):
    with open (Filename, 'r') as file:
        lines = file.read().split()
        firstTwoLetters = lines[1]
        if firstTwoLetters == "SY":
            print(firstTwoLetters)
        else:
            continue



#Problem 3
#given a list of strings as an argument, checks for joined pairs
#where the first ends with "-" and the beginning ends with "-"
#print each pair and remove the hyphens

def wordPairs(list):
    #cycle through each word and look for a hyphen at the end
    for i in list:
        j = i + 1
        if i[-1] == '-':
            for j in list: #this is trying to look at the next item but I am a little confused
                if j[0] == '-':
                    newWord = i[:-1] + j[0:]
                    print(newWord)

        #HAD TO REFERENCE THE COMMAND FOR THE CHARACTER AT THE END OF A LIST



#Problem 4
#RAN OUT OF TIME
#MY PROGRAMMING CAN USE SOME WORK