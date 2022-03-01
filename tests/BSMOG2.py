from __future__ import print_function
from imutils.video import VideoStream
import imutils
import numpy as np
import cv2 as cv
import time

user = "admin"
password = "@ezakmi1105"
ip = "192.168.1.35"

# Source address
rtsp_url = "rtsp://{user}:{passw}@{ip}:554/h264/ch{ch}/main/av_stream"

video_source = rtsp_url.format(user = user, passw = password, ip =ip, ch = 1) 

model = ""

if model == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()
    
capture = VideoStream(video_source).start()

while True:
    start_time = time.time()
    frame = capture.read()
    
    if frame is None:
        break
    
    fgMask = backSub.apply(frame)
    
    thresh = cv.dilate(fgMask, None, iterations=2)    
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    imageArea = frame.shape[0] * frame.shape[1]
    
    result = list(map(lambda x: cv.contourArea(x) > (imageArea*0.001), cnts))   
    index = np.argwhere(result) 
    
    if(len(index)>0):
        print("Movement detected")
    else:
        print("Normal")
    
    frames = np.round(1/(time.time() - start_time))
    
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(frames), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    
    
    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)
        
    keyboard = cv.waitKey(27)
    if keyboard == 'q' or keyboard == 27:
        break