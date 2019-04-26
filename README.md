# Liquid flow_controler
Try to figure out how to control a flow of liquid (water, beer, wine,...) and to count the liquides passed through.

## Sources of inspiration :
- [Motor 12VDC + mosfet + resistanc](http://wiki.mchobby.be/index.php?title=Mini_Kit_Moteur_Hobbyiste)
- [Adafruit tutorial and code from Github](https://github.com/adafruit/Adafruit-Flow-Meter)

Connect the red wire to +5V, the black wire to common ground and the yellow sensor wire to pin #2.


## Products / devices
1. Raspberry PI3B+
2. [Flowmetter]

## Application Mock-up
Here you can find the first draft of the application [mock-up](https://balsamiq.cloud/shvcvri/p4m89qh/r2278?f=N4IgUiBcAMA0IDkpxAYWfAMhkAhHAsjgFo4DSUA2gLoC%2BQA%3D
).

## Webhooks doc
Here a snippet of a code i found [here](https://cmsdk.com/python/how-to-setup-a-raspberry-pi-to-receive-webhooks.html)

```bash
from time import sleep
from flask import Flask, request
import unicornhat as unicorn
import light.py
app = Flask(__name__)
@app.route('/', methods = ['POST'])
def index():
    data = request.get_json()
    if data['orders/create'] == null:
        light.light() //lights uHat on new order creation
    return "Success"
```


## Flowmeter counter

```bash
#// if a plastic sensor use the following calculation
  // Sensor Frequency (Hz) = 7.5 * Q (Liters/min)
  // Liters = Q * time elapsed (seconds) / 60 (seconds/minute)
  // Liters = (Frequency (Pulses/second) / 7.5) * time elapsed (seconds) / 60
  // Liters = Pulses / (7.5 * 60)
  float liters = pulses;
  liters /= 7.5;
  liters /= 60.0;
  ``
