#! /usr/bin/env python
import sys
import tkinter as tk
import time
import datetime
from threading import Thread
import json
import urllib.request
import urllib.parse
import urllib
import http.client

##GLOBALS##
ENCODING= 'utf-8'
HOST= 'http://127.0.0.1'
TEMP_HUM_PORT= 12345
COMMAND_PORT= 12346



class App():
  def __init__(self, parent):
    self.parent = parent
    #APP VARIABLES
    self.hum = tk.DoubleVar() 
    self.temp = tk.DoubleVar()

    self.frame = tk.Frame(master=parent)
    self.frame.pack(fill=tk.BOTH, expand = 1)
    
    self.initUI()
        
  
  def initUI(self):
    tk.Label(self.frame, text="Humidity").grid(row=0, column=0)
    tk.Label(self.frame, textvariable= self.hum).grid(row=0, column=1)   
    tk.Label(self.frame, text="%").grid(row=0, column=2)

    tk.Label(self.frame, text="Temperature").grid(row=1,column =0)
    tk.Label(self.frame, textvariable= self.temp).grid(row=1, column=1)
    tk.Label(self.frame, text= u'\N{DEGREE SIGN}' + "C").grid(row=1,column =2)
    
    hum_but = tk.Button(master=self.frame, text="HUMIDIFIER",command=humButton)
    heat_but = tk.Button(master=self.frame, text="HEATER",command=heatButton)
    heat_but.grid(row=2,column=0)
    hum_but.grid (row=2,column=1)   


STATE = {"temp":False,"hum":False}

def heatButton():
  print("TOGGLE HEATER")
  STATE["temp"] = not STATE["temp"]
  postJson("{}:{}".format(HOST,COMMAND_PORT),STATE)  


def humButton():
  print("TOGGLE HUMIDIFIER")
  STATE["hum"] = not STATE["hum"]
  postJson("{}:{}".format(HOST,COMMAND_PORT),STATE)


class SensorThread(Thread):
  def __init__(self,app):
    super(SensorThread,self).__init__()
    self.running = True
    self.app = app
  
  def stop(self):
    self.running = False
  
  def run(self):
    while self.running:
      time.sleep(5)#sensor updates its valeus every thirty seconds
      data = getJson("{}:{}".format(HOST,TEMP_HUM_PORT))
      self.app.hum.set(data['hum'])
      self.app.temp.set(data['temp'])      
  
 
def postJson(url, data):
  data = urllib.parse.urlencode(data)
  con = http.client.HTTPConnection("localhost", 12346)
  con.request("POST","",data)
  res = con.getresponse()
  return json.loads(res.read().decode(ENCODING))
       
def getJson(url):
  req = urllib.request.Request(url)
  res = urllib.request.urlopen(req)
  return json.loads(res.read().decode(ENCODING))


def main():
  root = tk.Tk()
  app = App(root)
  t = SensorThread(app)
  t.start()

  #c = CommandThread(app)
  #c.start()
  root.mainloop()
  t.stop()
  t.join()
 
if __name__ == '__main__':
  main()
