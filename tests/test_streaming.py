# import cv2 as cv

# vcap = cv.VideoCapture("rtsp://admin:@ezakmi1105@192.168.1.5:554/h264/ch1/main/av_stream")

# while(1):

#     ret, frame = vcap.read()
#     cv.imshow('VIDEO', frame)
#     cv.waitKey(1)
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()