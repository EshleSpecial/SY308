import config
import socket
import select
import sys
import pickle
from atm import *


class bank:
  def __init__(self):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.s.bind((config.local_ip, config.port_bank))
    #====================================================================
    # TO DO: Add any class variables your ATM needs in the __init__
    # function below this.  For example, user balances, PIN numbers
    # etc.
    #====================================================================
    self.userBalances = {'Alice': 100, 'Bob': 100, 'Carol':0}
    self.userPins = {'Alice': 1234, 'Bob': 9999, 'Carol': 0000}
  #Set up the three user accounts i.e Alice($100), Bob($100), Carol($0)
  #Input the pin numbers for the users 
  #Access the inserted.card file and the users.card files

  #====================================================================
  # TO DO: Modify the following function to handle the console input
  # Every time a user enters a command at the bank terminal, it comes
  # to this function as the variable "inString"
  # The current implementation simply sends this string to the ATM
  # as a demonstration.  You will want to remove this and instead process
  # this string to deposit money, check balance, etc.
  #====================================================================
  def handleLocal(self,inString):
    usrMsg = inString.split(" ")

    if(len(usrMsg) >= 2):
      usrCmd = usrMsg[0]
      usrName = usrMsg[1]
      if (usrCmd == 'balance'):
        try:
          print("$" + str(self.userBalances[usrName]) + "\n")
        except:
          print("Invalid User")
      if (usrCmd == 'deposit'):
        try:
          self.userBalances[usrName] += int(usrMsg[2])
          print("$" + str(usrMsg[2]) + " added to " + usrName + "'s account\n")
        except:
          print("Invalid Request. Deposit requires a valid user and an amount")
    else:
      print("Invalid Request")
    self.prompt()

    #Any input from the ATM comes to this function as a string
    #apply specific commands to the various function 

  #====================================================================
  # TO DO: Modify the following function to handle the atm request 
  # Every time a message is received from the ATM, it comes to this
  # function as "inObject".  You will want to process this message
  # and potentially allow a user to login, dispense money, etc.
  # You will then have to respond to the ATM by calling the send() 
  # function to notify the ATM of any action you approve or disapprove.
  # Right now it just prints any message sent from the ATM to the screen
  # and sends the same message back to the ATM.
  #====================================================================
  def handleRemote(self, inObject):
    atmMessage = inBytes.decode('utf-8')
    atmMessage = atmMessage.split(" ")
    atmRequest = atmMessage[0]
    atmUsr = atmMessage[1]

    if (atmRequest == 'balance'):
      balance = self.userBalances[atmUsr]
      response = "$" + str(balance) + "\n"
      response = response.encode("utf-8")
      self.sendBytes(response)
    
    if (atmRequest == 'withdraw'):
      balance = self.userBalances[atmUsr]
      amt = int(atmMessage[2])
      if (balance >= amt):
        self.userBalances[atmUsr] -= amt
        response = "$" + str(amt) + "dispended\n"
      else:
        response = "Insuffiecent Funds.\n"

      response = response.encode('utf-8')
      self.sendBytes(response)
    
    if (atmRequest == 'check'):
      response = "Invalid"
      cardPin = atmMessage[2].rstrip()


      if(atmUsr in self.userPins):
        if(int(self.userPins[atmUsr]) == int(cardPin)):
          response = "Valid"
      response = response.encode('utf-8')
      self.sendBytes(response)
    
    
    print("\nFrom ATM: ", inObject )
    self.send(inObject)



  #====================================================================
  # DO NOT MODIFY ANYTHING BELOW THIS UNLESS YOU ARE REALLY SURE YOU
  # NEED TO FOR YOUR APPROACH TO WORK. This is all the network IO code
  # that makes it possible for the ATM and bank to communicate.
  #====================================================================
  def prompt(self):
    sys.stdout.write("BANK:")
    sys.stdout.flush()

  def __del__(self):
    self.s.close()

  def sendBytes(self, m):
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
  b = bank()
  b.mainLoop()

