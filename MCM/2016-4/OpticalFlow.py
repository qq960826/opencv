__author__ = 'wzq'
import numpy as np
import cv2
import imutils
import numpy as np
import math

lk_params = {'winSize': (15, 15), 'maxLevel': 2,
             'criteria': (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)}

feature_params = {'maxCorners': 500, 'qualityLevel': 0.3, 'minDistance': 7, 'blockSize': 7}

track_len = 5
detect_interval = 1
tracks = []
cam = cv2.VideoCapture("/Users/wzq/Downloads/a~1.mp4")
#cam = cv2.VideoCapture("/Users/wzq/Downloads/VID_20160416_235456.3gp")

cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
frame_idx = 0
count_x=0
count_y=0
angle=0
dir_x=""
dir_y=""
while True:
    ret, frame = cam.read()
    frame = imutils.resize(frame, width=600)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    vis = frame.copy()
    #vis=frame_gray.copy()
    if len(tracks) > 0:
        img0, img1 = prev_gray, frame_gray
        p0 = np.float32([tr[-1] for tr in tracks]).reshape(-1, 1, 2)
        p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
        p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
        d = abs(p0 - p0r).reshape(-1, 2).max(-1)
        good = d < 1
        new_tracks = []
        for tr, (x, y), good_flag in zip(tracks, p1.reshape(-1, 2), good):
            if not good_flag:
                continue
            tr.append((x, y))
            if len(tr) > track_len:
                del tr[0]
            new_tracks.append(tr)
            #cv2.circle(vis, (x, y), 3, (0, 255, 0), 1)

        tracks = new_tracks
        #print(tracks)
        count_x=0
        count_y=0

        if len(tracks)>1:



            for possibility in range(len(tracks[0])):
                if possibility==len(tracks[0])-2 or len(tracks[0])<2:
                    break
                count_x+=tracks[0][possibility+1][0]-tracks[0][possibility][0]
                count_y+=tracks[0][possibility+1][1]-tracks[0][possibility][1]
        #print(str(count_x)+" "+str(count_y))
        cv2.polylines(vis, [np.int32(tr) for tr in tracks], False, (0, 255, 0))
        try:
            angle=math.atan(abs(count_y/count_x))
            angle=(angle*180)/math.pi
        except:
            angle=90

        # cv2.imshow('track count: %d' % len(tracks), vis)
        if np.abs(count_x)>15:
            if np.sign(count_x)==-1:
                dir_x="right"
            else:
                dir_x="left"
        else:
            dir_x=""
        if np.abs(count_y)>15:
            if np.sign(count_y)==-1:
                dir_y="down"
            else:
                dir_y="up"
        else:
            dir_y=""

    if frame_idx % detect_interval == 0:
        mask = np.zeros_like(frame_gray)
        mask[:] = 255
        for x, y in [np.int32(tr[-1]) for tr in tracks]:
            cv2.circle(mask, (x, y), 5, 0, -1)
        p = cv2.goodFeaturesToTrack(frame_gray, mask=mask, **feature_params)
        if p is not None:
            for x, y in np.float32(p).reshape(-1, 2):
                tracks.append([(x, y)])
    cv2.putText(vis, dir_x+","+dir_y+",angle:"+str(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 255), 3)
    frame_idx += 1
    prev_gray = frame_gray
    cv2.imshow('OpticalFlow', vis)
    cv2.imshow('test', frame_gray)
    ch = 0xFF & cv2.waitKey(50)
    if ch == 27:
        break
