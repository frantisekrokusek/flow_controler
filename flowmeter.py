from gpiozero import LineSensor
from signal import pause
import time, sys
import http.client


sensor = LineSensor(4)

global count
count = 0

def countPulse():
    global count
    count += 1
    liters = count / (7.5 * 60)
    print('%s Litres'%(liters));
    conn = http.client.HTTPSConnection('en03hwbtjrvx4g.x.pipedream.net')
    conn.request("POST", "/", '{ "pipe_name": "Pilsner"; "quantity": %s }' %(liters), {'Content-Type': 'application/json'})

sensor.when_line = countPulse