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
print("Connection ready!")


try:
    while True:
        data_raw = ser.readline()
        try:
            print(data_raw.decode('latin-1'))
            data = json.loads(data_raw.decode('latin-1'), strict=False)
        except json.decoder.JSONDecodeError:
            print('The string does not contain valid JSON')
        except UnicodeDecodeError:
            print('Incorrect decoding')
finally:
    print("Closing serial connections...")
    ser.close()
    time.sleep(.1)
