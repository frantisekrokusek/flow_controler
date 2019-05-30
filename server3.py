import os
from gpiozero import LineSensor
from gpiozero import LED
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import json
from websocket import create_connection
from signal import pause
import time

vanne = LED(17)
sensor = LineSensor(4)



def send_ws():
    global count
    global wsd
    global mousse_qr_code
    count += 1
    litres = count / 200
    wsd.send('{"command":"message","identifier":"{\\"channel\\":\\"TransacChannel\\",\\"mousse_qr_code\\":\\"%s\\"}","data":"{\\"Litres\\":\\"%s\\",\\"mousse_qr_code\\":\\"%s\\"}"}'%(mousse_qr_code, litres, mousse_qr_code))
    print('%s Litres Sent'%(litres))

def counter():
    while True:
        time.clock()
        if time.clock() > 20 :
            print('waited too long')
            vanne.off()
            break
        else:
            sensor.when_line = lambda: send_ws()

def child():
   print('\nA new child process ',  os.getpid())
   global mousse_qr_code
   mousse_qr_code = "lewagon242"
   global wsd
   wsd = create_connection("ws://10.0.0.33:3000/cable")
   wsd.send('{"command":"subscribe","identifier":"{\\"channel\\":\\"TransacChannel\\",\\"mousse_qr_code\\":\\"%s\\"}"}'%(mousse_qr_code))
   global count
   count = 0
   time.sleep(2)
   print("Prepared to send informations...")
   vanne.on()
   counter()
   os._exit(0)

def parent():
  while True:
    newpid = os.fork()
    if newpid == 0:
      try:
          http_server = tornado.httpserver.HTTPServer(application)
          http_server.listen(8000)
          main_loop = tornado.ioloop.IOLoop.instance()
          print("Tornado Server started")
          main_loop.start()
      except:
          print("Exception triggered - Tornado Server stopped.")
          vanne.off()
          break
    else:
      continue


class MainHandler(tornado.web.RequestHandler):
  def post(self):
     print("Request received")
     data = self.request.body
     print(data)
     d = json.loads(data.decode('utf-8'))
     if d['unlocked'] == "true":
         print("Mousse is valid, and unlocking !")
         child()
     elif d['unlocked'] == "false":
         print("Mousse is locked !")
         vanne.off()
     else:
         print("Mousse qr_code is wrong!")

application = tornado.web.Application([(r'/', MainHandler)])


parent()


