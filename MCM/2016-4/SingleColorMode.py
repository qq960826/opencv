__author__ = 'wzq'

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import math

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())


greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

pts = deque(maxlen=args["buffer"])
counter = 0
angle=0
(dX, dY) = (0, 0)
direction = ""


if not args.get("video", False):
	camera = cv2.VideoCapture(0)

else:
	camera = cv2.VideoCapture(args["video"])

while True:
	(grabbed, frame) = camera.read()
	if args.get("video") and not grabbed:
		break

	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)


	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	if len(cnts) > 0:

		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		if radius > 10:

			pts.appendleft(center)
	for i in np.arange(1, len(pts)):

		if pts[i - 1] is None or pts[i] is None:
			continue

		if counter >= 10 and i == 1 and pts[-10] is not None:

			dX = pts[-10][0] - pts[i][0]
			dY = pts[-10][1] - pts[i][1]
			(dirX, dirY) = ("", "")


			if np.abs(dX) > 8:
				dirX = "East" if np.sign(dX) == 1 else "West"


			if np.abs(dY) > 8:
				dirY = "North" if np.sign(dY) == 1 else "South"

			if dirX != "" and dirY != "":
				try:
					angle=(math.acos(math.fabs(dX/math.sqrt(dX*dX+dY*dY)))*180)/math.pi
				except:
					angle=0
				direction = "{}-{}-{}".format(dirY, dirX,angle)

			else:
				direction = dirX if dirX != "" else dirY

		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)

	cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 255), 3)
	cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

	cv2.imshow("Frame", frame)
	cv2.imshow("mask", mask)
	key = cv2.waitKey(1) & 0xFF
	counter += 1

	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()