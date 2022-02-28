import time
import cv2
import utils

class Yolo():

    _cutils = utils.Utils()

    _config_name = "yolo.cfg"
    _weights_name = "yolo.weights"
    _coco_file = "coco.names"
    _conf_threshold=0.6
    _nms_threshold=0.4

    _model = None

    _init_time = 0
    _detection_time = 0
    _postprocess_time = 0

    def __init__(self, root = "./sources/yolo/"):        
        self.root = root     
        with open(self._cutils.join_path(root, self._coco_file), 'r') as f:
            self._classes = f.read().splitlines()

    def initModel(self):
        start_time = time.time()
        #Formatting paths 
        self._config_name = self._cutils.join_path(self.root, self._config_name)
        self._weights_name = self._cutils.join_path(self.root, self._weights_name)
        self._coco_file = self._cutils.join_path(self.root, self._coco_file)
        #Model initialization
        net = cv2.dnn.readNet(self._weights_name, self._config_name)
        self._model = cv2.dnn_DetectionModel(net)
        self._model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)
        #Get processing time
        self._init_time = time.time() - start_time

    def detect(self, frm):
        start_time = time.time()
        #Getting predictions of an input
        detections =  self._model.detect(frm, confThreshold=self._conf_threshold, 
                                    nmsThreshold=self._nms_threshold)
        #Get processing time
        self._detection_time = time.time() - start_time
        return detections


    def post_process(self, outs, frm):
        start_time = time.time()
        #Post processing the image with the output predictions
        for (classId, score, box) in zip(outs[0], outs[1], outs[2]):
            if classId == 0:
                cv2.rectangle(frm, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                            color=(0, 255, 0), thickness=2)
                text = '%s: %.2f' % (self._classes[classId], score)
                cv2.putText(frm, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            color=(0, 255, 0), thickness=3)
        #Get processing time
        self._postprocess_time = time.time() - start_time

    def set_configFile(self, config):
        self._config_name = config

    def set_weights(self, weights):
        self._weights_name = weights

    def set_cocoNames(self, names):
        self._coco_file = names
    
    def set_confThreshold(self, threshold):
        self._conf_threshold = threshold

    def set_NMSThreshold(self, threshold):
        self._nms_threshold = threshold
    
    def get_init_time(self):
        return self._init_time
    
    def get_detection_time(self):
        return self._detection_time
    
    def get_postprocess_time(self):
        return self._postprocess_time
