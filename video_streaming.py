from imutils.video import VideoStream
from random import random
from enum import Enum, unique
from flask import jsonify
from detectors.utils import Utils
from detectors.yolov4 import Yolo
from detectors.ssd import SSD
from db_manager.detections_model import  Detection
from threading import Thread
import imutils
import numpy as np
import cv2 as cv
import time
import datetime
import os

@unique
class Model(Enum):
    YOLOv4 = 1
    YOLOv4Tiny = 2
    SDD = 3

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
        self.frames_processed = 0
             
        
    def init_connection_to_ctv(self):        
        url = self.system["link"].format(ch = self.transmition)
        self.source = VideoStream(url).start()
    
    def init_model_detection(self):
        self.model = Model(self.system["model"])
        self.root = os.path.dirname(__file__)
        self.backSub = cv.createBackgroundSubtractorKNN()
        if(self.model is Model.YOLOv4Tiny):
            sources = self.utils.join_path(self.root,"models/yolo")
            self.yolo = Yolo(root = sources)
            self.yolo.set_weights("pretrained_yolov4-tiny.weights")
            self.yolo.set_configFile("pretrained_yolov4-tiny.cfg")
            self.yolo.set_confThreshold(0.55)
            self.yolo.initModel()
        elif(self.model is Model.SDD):
            sources = self.utils.join_path(self.root,"models/ssd")
            self.ssd = SSD(root = sources)
            self.ssd.init_model()

    def stream(self):
        init = 1
        while not self.thread_stop_event.is_set():
            start_time = time.time()
            frame = self.source.read()
            if frame is not None:                
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
                    if (not self.thread.is_alive()) and self.frames_processed > 100:
                        self.frames_processed = 0
                        self.thread = Thread(target=self._save_detection, args=({
                            "id": 0,
                            "system": self.system["id"],
                            "camera": self.camera,
                            "model": self.model.name,
                            "detection_time": datetime.datetime.now(),
                            "image": frame,
                            "movement": True,
                            "person": (len(outs[0])>0)
                        },))
                        self.thread.start()
                    else:
                        self.frames_processed = self.frames_processed + 1
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
                print("Image sent - Init: ", init)
                init = init + 1
                print("Tiempo estimado: ", ((time.time() - start_time)))
                self.socket.sleep(0)
        self.source.close()
        
    def _movement_detection(self, frame):
        fgMask = self.backSub.apply(frame)    
        thresh = cv.dilate(fgMask, None, iterations=2)    
        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)                
        imageArea = frame.shape[0] * frame.shape[1]                
        result = list(map(lambda x: cv.contourArea(x) > (imageArea*0.005), cnts))   
        index = np.argwhere(result)
        return len(index)
    
    def set_database_manager(self, database):
        self.database = database
    
    def _save_detection(self, data):
        today = datetime.datetime.now()
        name = str(today.date()) + "_" + str(today.time()).replace('.','-').replace(':','-') + "_" + self.system["name"] + "_camera" + str(self.camera) + ".png"
        # save = self.utils.join_path(self.image_root, name)
        try:
            os.chdir(self.image_root)
            cv.imwrite(name, data["image"])
            os.chdir(self.root)
            # img_bytes = cv.imencode('.png', data["image"])[1].tobytes()
            # f = open(name, "wb")
            # f.write(img_bytes)
            # f.close()
            data["image"] = name
            detection = Detection()
            if detection.add_detection(data, self.database) is None:
                # time.sleep(2)
                print("Detection not added")
            else:
                # time.sleep(15)
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