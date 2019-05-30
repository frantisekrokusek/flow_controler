from websocket import create_connection
from signal import pause
import time
from gpiozero import LineSensor
from gpiozero import LED

vanne = LED(17)
sensor = LineSensor(4)

mousse_qr_code = "lewagon242"

wsd = create_connection("ws://10.0.0.33:3000/cable")
wsd.send('{"command":"subscribe","identifier":"{\\"channel\\":\\"TransacChannel\\",\\"mousse_qr_code\\":\\"%s\\"}"}'%(mousse_qr_code))
time.sleep(3)
print("Prepared to send informations...")
vanne.on()

global count
count = 0

def test():
    global count
    count += 1
    litres = count / 200
    wsd.send('{"command":"message","identifier":"{\\"channel\\":\\"TransacChannel\\",\\"mousse_qr_code\\":\\"%s\\"}","data":"{\\"Litres\\":\\"%s\\",\\"mousse_qr_code\\":\\"%s\\"}"}'%(mousse_qr_code, litres, mousse_qr_code))
    print('%s Litres Sent'%(litres))
        
def counter():
    while True:
        time.clock()
        if time.clock() > 100 :
            print('waited too long')
            vanne.off()
            break
        else:
            sensor.when_line = lambda: test()

counter()

