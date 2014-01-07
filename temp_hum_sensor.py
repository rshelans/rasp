#! /usr/bin/env python2.7
import time
from threading import Thread
import subprocess
import sys
import BaseHTTPServer
import json

###GLOBALS####
ENCODING= 'utf-8'
HOST= '127.0.0.1'    
PORT= 12345


class Sensor():
  def __init__(self):
    self.data = {}
    self.data["temp"] = float()
    self.data["hum"] = float()

class TempHumiditySensorThread(Thread):
  def __init__(self, sensor):
    super(TempHumiditySensorThread, self).__init__()
    self.running = True
    self.sensor = sensor

  def stop(self):
    self.running = False
   
  def run(self):
    print("Temperatur Humidity Sensor Started")
    while self.running:
      time.sleep(5)#sensor updates its valeus every thirty seconds
      #sample Sensor
      data = self.getDataFromAda()
      if data:
        self.sensor.data["temp"] = data["temp"]
        self.sensor.data["hum"]  = data["hum"]

  #parses data from the adafruit driver program and gets out the temp/hum
  def getDataFromAda(self):
    data = subprocess.check_output(["./Adafruit_DHT", "22", "4"])
    data.decode(ENCODING)
    data = [float(s) for s in data.split() if is_float(s)]    
    if len(data) != 2:
      return None 
    return {'temp':data[0],'hum':data[1]}

def is_float(s):
  try:
    float(s)
    return True
  except:
    return False

class TempHumHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  #def __init__(self,sensor):
  #  super(TempHumHandler, self).__init__()
  #  self.running = True
  #  self.sensor = sensor

  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','application/json')
    self.end_headers()
    ##WRITE GET RESPONSE##
    self.wfile.write(json.dumps(self.sensor.data))


#Main thread sets up server for inter pi connections. starts the sensor thread.
#then sits and waits for connnections. Following a connections it holds a
#Reference to the socket and replys every so often with the valeus of the sensor
#Boiler Plat Command Line runnable calls main.  
if __name__ == '__main__':
  sensor = Sensor()
  t  = TempHumiditySensorThread(sensor)
  t.start()
  try:
    print("Temperatur Humidity Server Started")
    handler = TempHumHandler
    handler.sensor = sensor
    httpd = BaseHTTPServer.HTTPServer(('',PORT),handler)
    httpd.serve_forever()
  except KeyboardInterrupt:
    print() 
    print("Clean Up and Exit...")
    t.stop()
    t.join()
    
