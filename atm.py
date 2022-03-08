import config
import socket
import select
import sys
import json
import pickle
from bank import *


class atm:
  def __init__(self):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.s.bind((config.local_ip, config.port_atm))
    #====================================================================
    # TO DO: Add any class variables your ATM needs in the __init__
    # function below this.  I have started with two variables you might
    # want, the loggedIn flag which indicates if someone is logged in to
    # the ATM or not and the user variable which holds the name of the
    # user currently logged in.
    #====================================================================
    self.currentUsr = None


  #====================================================================
  # TO DO: Modify the following function to handle the console input
  # Every time a user enters a command at the ATM terminal, it comes
  # to this function as the variable "inString"
  # The current implementation simply sends this string to the bank
  # as a demonstration.  You will want to remove this and instead process
  # this string and determine what, if any, message you want to send to
  # the bank.
  #====================================================================
  def handleLocal(self,inString):
    self.send(inString)
    usrInput = inString.split(" ")
    command = usrInput[0]
    atmMessage = ""

    if (command == 'begin-session'):
      if (self.currentUsr == None):
        with open("Inserted.card", 'r') as cardFile:
          usr = cardFile.readline().rstrip()
          cardPin = cardFile.readline().rstrip()
          #checks if user has an account
          message = "check " + usr + " " + cardPin
          self.sendBytes(bytes(message, 'utf-8'))
          boolean, response = self.recvBytes()
          response = response.decode("utf-8")
          if response == 'valid':
            print("Welcome " + usr)
            pin = input(" Please enter your pin: ")
            if (pin.rstrip() == cardPin.rstrip()):
              print(" Authorized.\n")
              self.currentUsr = str(usr)
            else:
              print(" Unauthorized\n")
              self.prompt()
          else:
            print(response)
            print("\n You are not a valid user. Please insert a valid ATM user account card.\n")
            self.prompt()
      else:
        print("\n Welcome, " + self.currentUsr.rstrip() + ", you strated a session!\n")
        self.prompt()
    elif (command == 'end-session'):
      if(self.currentUsr == None):
        print("\n No User is currently logged in\n")
      else:
        print("\n " + self.currentUsr + " logged out\n")
        self.currentUsr = None
        self.prompt()
    elif (command == 'withdraw'):
      if(self.currentUsr == None):
        print("\n No user is currently logged i\n")
        self.prompt()
      else:
        try:
          amt = str(usrInput[1])

          #FAIL SAFE
          if(all(a.isdigit() == True for a in amt)):
            amtMessage = command + " " + self.currentUsr.rstrip() + " " + str(abs(int(amt)))
            self.sendBytes(bytes(atmMessage, 'utf-8'))
          else:
            print(" Amount must be a positive integer\n")
            self.prompt()
        except IndexError:
          print("\n Withdraw requires an amount\n")
          self.prompt()
  

  #====================================================================
  # TO DO: Modify the following function to handle the bank's messages.
  # Every time a message is received from the bank, it comes to this
  # function as "inObject".  You will want to process this message
  # and potentially allow a user to login, dispense money, etc.
  # Right now it just prints any message sent from the bank to the screen.
  #====================================================================
  def handleRemote(self, inObject):
    print("From Bank: ", inObject)


  #====================================================================
  # DO NOT MODIFY ANYTHING BELOW THIS UNLESS YOU ARE REALLY SURE YOU
  # NEED TO FOR YOUR APPROACH TO WORK. This is all the network IO code
  # that makes it possible for the ATM and bank to communicate.
  #====================================================================
  def prompt(self):
    print("ATM" + (" (" + self.user + ")" if self.user != None else "") + ":", end="")
    sys.stdout.flush()

  def __del__(self):
    self.s.close()

  def send(self, m):
    self.s.sendto(pickle.dumps(m), (config.local_ip, config.port_router))

  def recvBytes(self):
      data, addr = self.s.recvfrom(config.buf_size)
      if addr[0] == config.local_ip and addr[1] == config.port_router:
        return True, data
      else:
        return False, bytes(0)

  def mainLoop(self):
    self.prompt()
  
    while True:
      l_socks = [sys.stdin, self.s]
           
      # Get the list sockets which are readable
      r_socks, w_socks, e_socks = select.select(l_socks, [], [])
           
      for s in r_socks:
        # Incoming data from the router
        if s == self.s:
          ret, data = self.recvBytes()
          if ret == True:
            self.handleRemote(pickle.loads(data)) # call handleRemote 
            self.prompt() 
            
                                 
        # User entered a message
        elif s == sys.stdin:
          m = sys.stdin.readline().rstrip("\n")
          if m == "quit": 
            return
          self.handleLocal(m) # call handleLocal
          self.prompt() 
    
         
if __name__ == "__main__":
  a = atm()
  a.mainLoop()
    
