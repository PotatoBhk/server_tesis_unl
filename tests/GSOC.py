from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
import cv2 as cv
import time

user = "admin"
password = "@ezakmi1105"
ip = "192.168.1.35"

# Source address
rtsp_url = "rtsp://{user}:{passw}@{ip}:554/h264/ch{ch}/main/av_stream"

video_source = rtsp_url.format(user = user, passw = password, ip =ip, ch = 1) 

background_subtr_method = cv.bgsegm.createBackgroundSubtractorGSOC()
    
capture = VideoStream(video_source).start()

while True:
    # read video frames
    start_time = time.time()
    frame = capture.read()
    # check whether the frames have been grabbed
    if frame is None:
        break
    # resize video frames
    frame = cv.resize(frame, (640, 360))
    # pass the frame to the background subtractor
    foreground_mask = background_subtr_method.apply(frame)
    # obtain the background without foreground mask
    background_img = background_subtr_method.getBackgroundImage()
    frames = np.round(1/(time.time() - start_time))
    
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(frames), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    
    # show the current frame, foreground mask, subtracted result
    cv.imshow("Initial Frames", frame)
    cv.imshow("Foreground Masks", foreground_mask)
    cv.imshow("Subtraction Result", background_img)
    
    keyboard = cv.waitKey(27)
    if keyboard == 'q' or keyboard == 27:
        break
 

