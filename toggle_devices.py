#! /usr/bin/env python
import sys
import subprocess
import json
import http.server
import RPi.GPIO as IO
###GLOBALS####
ENCODING= 'utf-8'
HOST= "127.0.0.1"  
PORT=     12346
HUM_PIN=23
HEAT_PIN=24


#### ALLL MESSAGES MUST END WITH A \n ##########


class SwitchVar():
   def __init__(self, state = False):
     self.data = {"temp":state,"hum":state}
     
#Main thread sets up server for inter pi connections. starts the sensor thread.
#then sits and waits for connnections. Following a connections it holds a
#Reference to the socket and replys every so often with the valeus of the sensor
#Boiler Plat Command Line runnable calls main.  
 
class ToggleHandler(http.server.BaseHTTPRequestHandler):
  def do_POST(self):
    self.send_response(200)
    self.send_header('Content-type','application/json')
    self.end_headers()

    content_length = int(self.headers['Content-Length'])
    content = self.rfile.read(content_length)
    content = parsePostString(content.decode(ENCODING))
    self.switch.data['temp'] = (content['temp'] == "true" or  content['temp']=="True" )
    self.switch.data['hum']  = (content['hum'] == "true"  or "True" == content['hum'] )
    IO.output(HUM_PIN,self.switch.data['hum'])
    IO.output(HEAT_PIN,self.switch.data['temp'])
        
 
    ##STUB-- Do stuff when post occures
    ##Write the Post Data Back to the client
    self.wfile.write(json.dumps(content).encode(ENCODING))

  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','application/json')
    self.end_headers()

    ##WRITE GET RESPONSE##
    self.wfile.write(json.dumps(self.switch.data).encode(ENCODING))


def parsePostString(s):
  mapping = dict()
  for key,val in [x.split("=") for x in s.split("&")]:
    mapping[key] = val
  return mapping

if __name__ == '__main__':
  print("Toggle Server on {}:{} started.".format(HOST,PORT))
  
  IO.setmode(IO.BCM)
  IO.setup(HEAT_PIN,IO.OUT)
  IO.setup(HUM_PIN,IO.OUT)
  #initialize to off
  IO.output(HUM_PIN,False)
  IO.output(HEAT_PIN,False)
  try:
    handler = ToggleHandler
    handler.switch = SwitchVar()
      
    httpd = http.server.HTTPServer(('',PORT),handler)
    httpd.serve_forever()
  except KeyboardInterrupt:
    print("Good-Bye")
    IO.cleanup()
