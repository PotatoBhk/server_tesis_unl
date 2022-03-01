from imutils.video import VideoStream
from random import random
from enum import Enum, unique
from detectors.utils import Utils
from detectors.yolov4 import Yolo
from detectors.ssd import SSD
from db_manager.detections_model import  Detection
import imutils
import numpy as np
import cv2 as cv
import time
import os

@unique
class Model(Enum):
    YOLOv4 = 1
    YOLOv4Tiny = 2
    SDD = 3

class VideoStreaming():    
    
    def __init__(self, socket, thread_stop_event, system, transmition:str):
        #TODO Make function for Websockets Connections
        print("Init Video Streaming Class...")
        self.socket = socket
        self.thread_stop_event = thread_stop_event
        self.system = system
        self.transmition = transmition
        self.utils = Utils()
        self.timeout = 0
    
    def randomNumberGenerator(self):
        #infinite loop of magical random numbers
        print("Making random numbers")
        while not self.thread_stop_event.is_set():
            number = round(random()*10, 3)
            print(number)
            self.socket.emit('newnumber{tr}'.format(tr=self.transmition), str(number))
            self.socket.sleep(5)
             
        
    def init_connection_to_ctv(self):        
        url = self.system["link"].format(ch = self.transmition)
        self.source = VideoStream(url).start()
    
    def init_model_detection(self):
        self.model = Model(self.system["model"])
        root = os.path.dirname(__file__)
        self.backSub = cv.createBackgroundSubtractorKNN()
        if(self.model is Model.YOLOv4Tiny):
            sources = self.utils.join_path(root,"models/yolo")
            self.yolo = Yolo(root = sources)
            self.yolo.set_weights("pretrained_yolov4-tiny.weights")
            self.yolo.set_configFile("pretrained_yolov4-tiny.cfg")
            self.yolo.initModel()
        elif(self.model is Model.SDD):
            sources = self.utils.join_path(root,"models/ssd")
            self.ssd = SSD(root = sources)
            self.ssd.init_model()

    def stream(self):
        init = 1
        while not self.thread_stop_event.is_set():
            start_time = time.time()
            frame = self.source.read()
            if frame is not None:
                self.timeout = 0
                #Movement detection                
                if(self._movement_detection(frame) > 0):
                    #Object detection
                    if(self.model is Model.YOLOv4Tiny):
                        outs = self.yolo.detect(frame)
                        self.yolo.post_process(outs,frame)
                    elif(self.model is Model.SDD):
                        detections = self.ssd.detect(frame)
                        outs = self.ssd.format_output(detections)
                        self.ssd.postprocess(frame, outs)                        
                    self.socket.emit('detection{tr}'.format(tr=self.transmition), 
                                     {"movement": True, "detection": (len(outs[0])>0)})
                else:
                    self.socket.emit('detection{tr}'.format(tr=self.transmition),
                                     {"movement": False, "detection": False})
                #Image to bytes transformation
                img_bytes = cv.imencode('.jpg', frame)[1].tobytes()
                self.socket.emit('video{tr}'.format(tr=self.transmition), img_bytes)
                print("Image sent - Init: ", init)
                init = init + 1
                print("Tiempo estimado: ", ((time.time() - start_time)))
                self.socket.sleep(5)
            else:
                if(self.time < 10):
                    time.sleep(2)
                    self.time = self.time + 2
                else:
                    break
        self.source.close()
        
    def _movement_detection(self, frame):
        fgMask = self.backSub.apply(frame)    
        thresh = cv.dilate(fgMask, None, iterations=2)    
        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)                
        imageArea = frame.shape[0] * frame.shape[1]                
        result = list(map(lambda x: cv.contourArea(x) > (imageArea*0.001), cnts))   
        index = np.argwhere(result)
        return len(index)