import numpy as np
import cv2
import time
from utils import Utils

class SSD():
    #Labels of network.
    _classNames = { 0: 'background',
        1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
        5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
        10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
        14: 'motorbike', 15: 'person', 16: 'pottedplant',
        17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor' }
    
    _prototxt_name = "deploy.prototxt"
    _weights_name = "model.caffemodel"
    _threshold = 0.6
    _init_time = 0
    _detection_time = 0
    _format_time = 0

    _net = None

    _utils = Utils()
    
    def __init__(self, root = "./sources/ssd/"):
        self.root = root
    
    def init_model(self):
        start_time = time.time()
        #Get model's paths
        prototxt = self._utils.join_path(self.root, self._prototxt_name)
        weights = self._utils.join_path(self.root, self._weights_name)
        #Model initialization
        self._net = cv2.dnn.readNetFromCaffe(prototxt, weights)
        #Get processing time
        self._init_time = time.time() - start_time

    def detect(self, frame, shape = (300, 300)):      
        start_time = time.time()
        #Preprocess image
        input = self._utils.preprocess_img(frame, shape)
        #Get predictions of an input      
        self._net.setInput(input)
        detections = self._net.forward()
        #Get processing time
        self._detection_time = time.time() - start_time
        return detections

    def format_output(self, detections):
        start_time = time.time()
        #Get the index of valid detections defined by a threshold
        index = np.argwhere(detections[0][0][:,2]>self._threshold)
        index = index[:,0]
        #Formating outputs
        class_ids = detections[0][0][index,1]
        scores = detections[0][0][index,2]
        x_points = np.vstack((detections[0][0][index,3], detections[0][0][index,5])).T
        y_points = np.vstack((detections[0][0][index,4], detections[0][0][index,6])).T
        #Get processing time
        self._format_time = time.time() - start_time
        return class_ids, scores, x_points, y_points

    def postprocess(self, frame, out, resized_shape = (300, 300)):
        class_ids, scores, x_points, y_points = out

        heightFactor = frame.shape[0]/resized_shape[0] 
        widthFactor = frame.shape[1]/resized_shape[1]

        x_points = np.multiply(x_points, (resized_shape[1] * widthFactor)).astype(np.dtype(int))
        y_points = np.multiply(y_points, (resized_shape[0] * heightFactor)).astype(np.dtype(int))

        for(class_id, score, x, y) in zip(
        class_ids, scores, x_points, y_points):
            cv2.rectangle(frame, (x[0], y[0]), (x[1], y[1]),
                                (0, 255, 0))
            label = self._classNames[class_id] + ": " + str(score)
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

            y_lb = max(y[0], labelSize[1])
            cv2.rectangle(frame, (x[0], y_lb - labelSize[1]),
                                    (x[0] + labelSize[0], y_lb + baseLine),
                                    (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, label, (x[0], y_lb),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
        return frame
    
    def set_prototxt(self, prototxt):
        self._prototxt_name = prototxt
    
    def set_weights(self, weights):
        self._weights_name = weights

    def set_threshold(self, threshold):
        self._threshold = threshold

    def get_initTime(self):
        return self._init_time
    
    def get_detectionTime(self):
        return self._detection_time
    
    def get_postprocessTime(self):
        return self._format_time