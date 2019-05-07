from gpiozero import LineSensor
from signal import pause
import time, sys
import httplib


sensor = LineSensor(4)

global count
count = 0

def countPulse():
    global count
    count += 1
    print(count);
    conn = httplib.HTTPSConnection('en03hwbtjrvx4g.x.pipedream.net')
    conn.request("POST", "/", '{ "pipe_name": "Pilsner"; "quantity": {count} }', {'Content-Type': 'application/json'})


sensor.when_line = countPulse
