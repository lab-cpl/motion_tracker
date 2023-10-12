import cv2
import os
import sys
from datetime import datetime


ID = sys.argv[1]
path = "/home/pi/images/" + ID + "/" + os.popen("date +'%Y-%m-%d_%H_%M'").read().strip()
os.system("mkdir -p " + path)
os.chdir(path)
video = cv2.VideoCapture(0)
video.set(3, 320)
video.set(4, 240)


frame_number = 0

try:
    while True:
        ret, img = video.read()
        date_ = str(datetime.now()).replace(" ", "_")
        filename = frame_number + "_" + "ID_" + ID + "_" + date_ + ".jpg"
        cv2.imwrite(filename, img)
        frame_number = frame_number + 1
except KeyboardInterrupt:
    pass


video.release()
