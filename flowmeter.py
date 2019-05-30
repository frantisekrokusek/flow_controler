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
    ws.send('Message')

sensor.when_line = countPulse
