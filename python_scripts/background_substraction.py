import numpy as np
import cv2

cap = cv2.VideoCapture("/home/nicoluarte/clip_test/out.mp4")

kernel = np.ones((3,3), np.uint8)
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

while(1):
    ret, frame = cap.read()
    frame = frame[70:210, 60:250]

    fgmask = fgbg.apply(frame)
    fgmask = cv2.erode(fgmask, kernel, iterations = 1)
    fgmask = cv2.dilate(fgmask, kernel, iterations = 2)
    contours, hierarchy = cv2.findContours(image=fgmask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        big_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(big_contour)
        if M["m00"] == 0:
            cx = 0
            cy = 0
        else:
            cx = int(np.true_divide(M["m10"] , M["m00"]))
            cy = int(np.true_divide(M["m01"] , M["m00"]))
            print(cx)
    image_copy = frame.copy()
    cv2.circle(image_copy, (cx, cy), 10, (255, 0, 0), 2)

    cv2.imshow('frame',image_copy)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
