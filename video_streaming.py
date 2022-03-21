from imutils.video import VideoStream
from random import random
from enum import Enum, unique
from detectors.utils import Utils
from detectors.yolov4 import Yolo
from db_manager.detections_model import  Detection
from threading import Thread
import imutils
import numpy as np
import cv2 as cv
import time
import datetime
import os
import random

@unique
class Model(Enum):
    PRETRAINED_YOLOV4 = 1
    PRETRAINED_YOLOV4_TINY = 2
    CUSTOM_YOLOV4_TINY = 3
    CUSTOM_YOLOV4_TINY2 = 4

class VideoStreaming():    
    
    def __init__(self, socket, thread_stop_event, system, transmition:str, camera:int):
        #TODO Make function for Websockets Connections
        print("Init Video Streaming Class...")
        root = os.path.dirname(__file__)
        self.socket = socket
        self.thread_stop_event = thread_stop_event
        self.system = system
        self.transmition = transmition
        self.camera = camera
        self.utils = Utils()
        self.thread = Thread()
        self.database = None
        self.image_root = self.utils.join_path(root, "images")
        self.detected = False
        self.wait_time = datetime.datetime.now()           
        
    def init_connection_to_ctv(self):        
        url = self.system["link"].format(ch = self.transmition)
        self.source = VideoStream(url).start()
    
    def init_model_detection(self):
        self.model = Model(self.system["model"])
        self.root = os.path.dirname(__file__)
        self.backSub = cv.createBackgroundSubtractorKNN(history=200, detectShadows=False)
        sources = self.utils.join_path(self.root,"models/yolo")
        self.yolo = Yolo(root = sources)
        self.yolo.set_weights(self.model.name + ".weights")
        self.yolo.set_configFile(self.model.name + ".cfg")
        self.yolo.set_confThreshold(0.60)
        self.yolo.initModel()

    def stream(self):
        init = 1
        while not self.thread_stop_event.is_set():
            start_time = time.time()
            frame = self.source.read()
            if frame is not None:                
                #Movement detection                
                if(self._movement_detection(frame) > 0):
                    #Object detection
                    outs = self.yolo.detect(frame)
                    self.yolo.post_process(outs,frame)                      
                    self.socket.emit('detection{tr}'.format(tr=self.transmition), 
                                     {"movement": True, "detection": (len(outs[0])>0)})
                    self._process_detection(frame, outs, (len(outs[0])>0))
                else:
                    self.socket.emit('detection{tr}'.format(tr=self.transmition),
                                     {"movement": False, "detection": False})
                frames = np.round(1/(time.time() - start_time))
                cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
                cv.putText(frame, "FPS: " + str(frames), (15, 15),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
                print("FPS: ", frames)
                #Image to bytes transformation
                scale_percent = 60 # percent of original size
                width = int(frame.shape[1] * scale_percent / 100)
                height = int(frame.shape[0] * scale_percent / 100)
                dim = (width, height)
                resized = cv.resize(frame, dim, interpolation = cv.INTER_AREA)              
                img_bytes = cv.imencode('.jpg', resized)[1].tobytes()
                self.socket.emit('video{tr}'.format(tr=self.transmition), img_bytes)
                if len(outs[0])>0:
                    self.socket.emit('detected', img_bytes)
                print("Image sent - Init: ", init)
                init = init + 1
                print("Tiempo estimado: ", ((time.time() - start_time)))
                self.socket.sleep(0)
        self.source.close()
        
    def _movement_detection(self, frame):
        fgMask = self.backSub.apply(frame)    
        thresh = cv.dilate(fgMask, None, iterations=2)    
        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)                
        imageArea = frame.shape[0] * frame.shape[1]                
        result = list(map(lambda x: cv.contourArea(x) > (imageArea*0.005), cnts))   
        index = np.argwhere(result)
        return len(index)
    
    def set_database_manager(self, database):
        self.database = database
    
    def _process_detection(self, frame, outs, detection):
        elapsed_time = datetime.datetime.now()

        if not self.detected:
            self.detected = True
            self.wait_time = elapsed_time + datetime.timedelta(seconds=10)
        
        if (not self.thread.is_alive()) and ((elapsed_time > self.wait_time) or detection):
            self.detected = False
            self.thread = Thread(target=self._save_detection, args=({
                "id": 0,
                "system": self.system["id"],
                "camera": self.camera,
                "model": self.model.name,
                "detection_time": elapsed_time,
                "image": frame,
                "movement": True,
                "person": (len(outs[0])>0)
            },))
            self.thread.start()

    def _save_detection(self, data):
        today = data["detection_time"]
        name = str(today.date()) + "_" + str(today.time()).replace('.','-').replace(':','-') + "_" + self.system["name"] + "_camera" + str(self.camera) + ".png"
        # save = self.utils.join_path(self.image_root, name)
        try:
            os.chdir(self.image_root)
            cv.imwrite(name, data["image"])
            os.chdir(self.root)
            data["image"] = name
            detection = Detection()
            if detection.add_detection(data, self.database) is None:
                print("Detection not added")
            else:
                print("Added..")
        except Exception as err:
            print("Image not written to root folder")
            print(err)
    
    def randomNumberGenerator(self):
        #infinite loop of magical random numbers
        print("Making random numbers")
        while not self.thread_stop_event.is_set():
            number = round(random()*10, 3)
            print(number)
            self.socket.emit('newnumber{tr}'.format(tr=self.transmition), str(number))
            self.socket.sleep(0)