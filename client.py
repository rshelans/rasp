#! /usr/bin/env python
import sys
import socket
import json

  


def main():
  host = socket.gethostname() 
  port = 12346

  s = socket.socket()
  c =  s.connect((host,port))
  try:
    s.sendall(r'{"state":"True"}'.encode('utf-8'))
    while(True):
      #data = json.loads(s.recv(1024).decode('utf-8'))
     
      data = s.recv(1024)
      s.sendall(data + "\n")
      print(data)

  except KeyboardInterrupt: 
    s.close()

if __name__ == '__main__':
  main()
