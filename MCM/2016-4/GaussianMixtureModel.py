__author__ = 'wzq'
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import math


pts = deque(maxlen=30)
mog=cv2.BackgroundSubtractorMOG()
counter = 0
(dX, dY) = (0, 0)
center = None
direction = ""
angle=0
camera = cv2.VideoCapture("/Users/wzq/Desktop/Untitled.mov")
mask=None
while True:
    (grabbed, frame) = camera.read()
    frame = imutils.resize(frame, width=600)
    if  not grabbed:
        break
    if counter==0:
        counter+=1
        continue
    mask=mog.apply(frame, None, 0.01);
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    if len(cnts)>0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 5:
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)
    if len(pts)>15:
        for i in np.arange(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue

            if counter >= 10 and i == 1 and pts[-10] is not None:
                dX = pts[-10][0] - pts[i][0]
                dY = pts[-10][1] - pts[i][1]
                (dirX, dirY) = ("", "")
                if np.abs(dX) > 5:
                    dirX = "left" if np.sign(dX) == 1 else "right"

                if np.abs(dY) > 5:
                    dirY = "up" if np.sign(dY) == 1 else "down"
                if dirX != "" and dirY != "":
                    try:

                        angle=(math.acos(math.fabs(dX/math.sqrt(dX*dX+dY*dY)))*180)/math.pi
                    except:
                        angle=0
                    direction = "{}-{}-{}".format(dirY, dirX,angle)


                else:
                    direction = dirX if dirX != "" else dirY
        cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,0.65, (0, 0, 255), 3)
    cv2.putText(frame, "dx: {}, dy: {}, angle:{}".format(dX, dY,angle),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)

    cv2.imshow("Gaussian Mixture Mode Mask",mask)
    cv2.imshow("Gaussian Mixture Mode Frame",frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    counter += 1