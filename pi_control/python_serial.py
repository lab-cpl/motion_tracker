import json
import os
import warnings
import time
import serial
import serial.tools.list_ports
import subprocess

arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'FT232R' in p.description  # may need tweaking to match new arduinos
]
if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')

print("arduino found")

print("Opening arduino connection...")
ser = serial.Serial(arduino_ports[0])
ser.baudrate = 115200
switch = 0
name = os.uname()[1]


try:
    while True:
        data_raw = ser.readline()
        try:
            data = json.loads(data_raw, strict=False)
            print(data['button_state'])
            if data['id'] == "a01":
                if data['button_state'] == True and switch == 1:
                    switch = 0
                    #os.system("export DISPLAY=:0")
                    #os.system("libcamera-vid -t 0  --width 1920 --height 1080 -p 100,100,1000,1000 --info-text '" + name + "' &")
                if data['button_state'] == False and switch == 0:
                    switch = 1
                    os.system("pkill python3")
        except json.decoder.JSONDecodeError:
            print('The string does not contain valid JSON')
finally:
    print("Closing serial connections...")
    ser.close()
    time.sleep(.1)
