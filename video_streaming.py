from imutils.video import VideoStream
import cv2
import time
from random import random
import asyncio

class VideoStreaming():    
    #Save on encrypted database
    user = "admin"
    password = "@ezakmi1105"
    ip = "192.168.1.35"
    
    # Source address
    rtsp_url = "rtsp://{user}:{passw}@{ip}:554/h264/ch{ch}/main/av_stream"

    def __init__(self, socket, thread_stop_event):
        #TODO Make function for Websockets Connections
        print("Init Video Streaming Class...")
        self.socket = socket
        self.thread_stop_event = thread_stop_event
        self.received = False
        self.wait = 5
    
    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        print("Making random numbers")
        while not self.thread_stop_event.is_set():
            number = round(random()*10, 3)
            print(number)
            self.socket.emit('newnumber', str(number))
            self.socket.sleep(5)
             
        
    def init_connection_to_ctv(self):
        #TODO Implement connection database
        self.video_source = self.rtsp_url.format(
            user = self.user, 
            passw = self.password, 
            ip = self.ip, 
            ch = 1
        )        
        self.source = VideoStream(self.video_source).start()
    
    def fn_received(self):
        self.received = True

    def stream(self):
        init = 0
        while not self.thread_stop_event.is_set():
            # if(self.received):
            self.received = False
            start_time = time.time()
            frame = self.source.read()
            img_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
            self.socket.emit('video', img_bytes)
            print("Image sent - Init: ", init)
            print("Tiempo estimado: ", ((time.time() - start_time)))
            self.socket.sleep(self.wait)
            
    def setWait(self, amount):
        self.wait = amount