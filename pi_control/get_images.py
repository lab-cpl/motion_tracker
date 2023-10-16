import time
from picamera2 import Picamera2
import cv2
import os
import sys
from datetime import datetime


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
    while True:
        img = video.capture_array()
        date_ = str(datetime.now()).replace(" ", "_")
        filename = str(frame_number) + "_" + "ID_" + ID + "_" + date_ + ".jpg"
        cv2.imwrite(filename, img)
        cv2.imwrite("/home/pi/Desktop/preview.jpg", img)
        frame_number = frame_number + 1
except KeyboardInterrupt:
    pass


video.close()
