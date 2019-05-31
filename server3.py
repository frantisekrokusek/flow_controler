import os
from gpiozero import LineSensor
from gpiozero import LED
# import RPi.GPIO as GPIO
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import json
from websocket import create_connection
from signal import pause
import time
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(11, GPIO.OUT)

vanne = LED(17)
sensor = LineSensor(4)

def child():
   def send_ws():
       global count
       global wsd
       global mousse_qr_code
       count += 1
       litres = count / 300
       wsd.send('{"command":"message","identifier":"{\\"channel\\":\\"TransacChannel\\",\\"mousse_qr_code\\":\\"%s\\"}","data":"{\\"Litres\\":\\"%s\\",\\"mousse_qr_code\\":\\"%s\\"}"}'%(mousse_qr_code, litres, mousse_qr_code))
       print('%s Litres Sent'%(litres))

   def counter():
       while True:
           time.clock()
           sensor.when_line = lambda: send_ws()
           if time.clock() > 10 :
               print('waited too long')
               wsd.send('{"command":"message","identifier":"{\\"channel\\":\\"TransacChannel\\",\\"mousse_qr_code\\":\\"%s\\"}","data":"{\\"mousse_qr_code\\":\\"%s\\",\\"unlocked\\":\\"false\\"}"}'%(mousse_qr_code, mousse_qr_code))
               break
           else:
               continue

   print('\nA new child process ',  os.getpid())
   global mousse_qr_code
   mousse_qr_code = "lewagon242"
   global wsd
   wsd = create_connection("wss://pomplamousse.herokuapp.com/cable")
   wsd.send('{"command":"subscribe","identifier":"{\\"channel\\":\\"TransacChannel\\",\\"mousse_qr_code\\":\\"%s\\"}"}'%(mousse_qr_code))
   global count
   count = 0
   time.sleep(2)
   print("Prepared to send informations...")
   vanne.on()
   counter()


class MainHandler(tornado.web.RequestHandler):
  def post(self):
     print("Request received")
     data = self.request.body
     print(data)
     d = json.loads(data.decode('utf-8'))
     if d['unlocked'] == "true":
         print("Mousse is valid, and unlocking !")
         # GPIO.output(11,True)
         vanne.on()
         child()
     elif d['unlocked'] == "false":
         print("Mousse is locked !")
         # GPIO.output(11,False)
         vanne.off()
     else:
         print("Mousse qr_code is wrong!")

application = tornado.web.Application([(r'/', MainHandler)])

try:
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8000)
    print("Tornado Server started")
    main_loop = tornado.ioloop.IOLoop.instance()
    main_loop.start()
except:
    print("Exception triggered - Tornado Server stopped.")
    # GPIO.output(11,False)
    vanne.off()



