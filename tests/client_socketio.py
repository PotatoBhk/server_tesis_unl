import socketio
import cv2
import numpy as np

# standard Python
sio = socketio.Client()
f = open("sample.jpg", "wb")

@sio.event
def connect():
    print("I'm connected!")

@sio.on('newnumber1')
def on_message(data):
    print("number 1: ", data)

@sio.on('newnumber2')
def on_message(data):
    print("number 2: ", data)

@sio.on('video')
def handle_video(data):
    image = np.asarray(bytearray(data), dtype="uint8")
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    print(img.shape)

sio.connect('http://127.0.0.1:5000')
# sio.emit('message', 'hola')
# sio.emit('another', 'hola')