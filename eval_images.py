from detectors.yolov4 import Yolo
from detectors.utils import Utils
import os

root = os.path.dirname(__file__)
utils = Utils()
sources = utils.join_path(root,"models/yolo")
yolo = Yolo(root = sources)
yolo.set_weights("pretrained_yolov4-tiny.weights")
yolo.set_configFile("pretrained_yolov4-tiny.cfg")
yolo.set_confThreshold(0.55)
yolo.initModel()