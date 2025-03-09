import time
from picamera2 import Picamera2
import cv2
import os
import sys
from datetime import datetime
import json
import warnings
import serial
import serial.tools.list_ports
import subprocess



# check for arduino port and open it
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
ms = "NA"
ser.close()
ser.open()
f = 1


def read_ms_from_serial():
    try:
        while True:
            # waits for message form arduino
            if(ser.inWaiting() > 0):
                data_raw = ser.readline()
                read = 1
            else:
                # if there is no message read = 0
                # so we pass an NA
                read = 0
                break
            try:
                data = json.loads(data_raw.decode('latin-1'), strict=False)
                if (read == 1):
                    try:
                        ms = int(data["time"])
                    except:
                        ms = "NA"
                err = 0
            except json.decoder.JSONDecodeError:
                err = 1
                print('The string does not contain valid JSON')
            except UnicodeDecodeError:
                err = 1
                print('Incorrect decoding')
            if err == 0:
                break
    finally:
        f = 0
    if read == 1 and (type(ms) == int or type(ms) == float):
        return(ms)
    else:
        return('NA')



ID = sys.argv[1]
path = "/home/pi/images/" + ID + "/" + os.popen("date +'%Y-%m-%d_%H_%M'").read().strip()
os.system("mkdir -p " + path)
os.chdir(path)
video = Picamera2()
video_config = video.create_video_configuration(main={"size": (320, 240)})
video.configure(video_config)
video.start()
time.sleep(2)
frame_number = 0

img = video.capture_array()
date_ = str(datetime.now()).replace(" ", "_")
cv2.imwrite("/home/pi/Desktop/preview.jpg", img)
os.system("rxvt -e sh -c 'bash /home/pi/scripts/run_preview.sh; bash' &")

try:
    print("starting frames . . .")
    while True:
        img = video.capture_array()
        ms = read_ms_from_serial()
        date_ = str(datetime.now()).replace(" ", "_")
        filename = str(frame_number) + "_" + str(ms) + "_" + "ID_" + ID + "_" + date_ + ".jpg"
        cv2.imwrite(filename, img)
        cv2.imwrite("/home/pi/Desktop/preview.jpg", img)
        frame_number = frame_number + 1
        print(filename)
except KeyboardInterrupt:
    pass


video.close()
ser.close()
