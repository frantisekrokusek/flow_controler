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



# une autre solution
# import RPi.GPIO as GPIO
# import time, sys

# FLOW_SENSOR = 4

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# global count
# count = 0

# def countPulse(channel):
#    global count
#    count = count+1
#    print(count);
# GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING, callback=countPulse)

# while True:
#     try:
#         time.sleep(1)
#     except KeyboardInterrupt:
#         print('\ncaught keyboard interrupt!, bye')
#         GPIO.cleanup()
#         sys.exit()
