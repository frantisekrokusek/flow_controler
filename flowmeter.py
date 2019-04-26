from gpiozero import LineSensor
from signal import pause
import time, sys

sensor = LineSensor(4)

global count
count = 0

def countPulse():
    global count
    count += 1
    print(count);

sensor.when_line = lambda: countPulse
sensor.when_no_line = lambda: print('No line detected')
pause()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print('\ncaught keyboard interrupt!, bye')
        GPIO.cleanup()
        sys.exit()
