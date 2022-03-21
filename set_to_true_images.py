from detectors.yolov4 import Yolo
from detectors.utils import Utils
import os
import cv2 as cv
import keyboard
import psycopg2

root = os.path.dirname(__file__)
utils = Utils()
source = utils.join_path(root,"images")
list_images = utils.winsort(os.listdir(source))

try:
    conn = psycopg2.connect(
        user = 'cieyttesis', 
        password = 'mpassword',
        database = 'unlobjdet'
    )
    print('Connected')
        
    cur = conn.cursor()
    for image in list_images:
      path = utils.join_path(source, image)
      img = cv.imread(path)
      cv.imshow("frame", img)
      cv.waitKey(0)
      if keyboard.read_key() == "t":
        cur.execute("UPDATE detections SET validated=true WHERE image='{}';".format(image))
        print("updated: " + image)
        conn.commit()
    cur.close() 
    conn.close()
except psycopg2.DatabaseError as error:
    print("Error en la base de datos: ", error)