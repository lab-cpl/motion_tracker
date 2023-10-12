# from utils import drawAxis, getOrientation
from utils import drawAxis, getOrientation
import numpy as np
import cv2
import argparse

# read in frame
cap = "/home/nicoluarte/raspberry_images/ID_550_2023-08-26_14:03:57.229828.jpg"
cap = cv2.imread(cap)

# show image
cv2.imshow('sample image', cap)
cv2.waitKey(0)
cv2.destroyAllWindows()

