from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from video_streaming import VideoStreaming
from threading import Thread, Event
from db_manager.database import Database
from db_manager.system_model import  System
from db_manager.users_model import User
# import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger = True, engineio_logger = True)

thread = Thread()
thread_stop_event = Event()

database = None

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods=['GET'])
def login():
    content = request.json
    user = User()
    response = user.validate_user(content, database.get_connection())
    return response

@app.route("/register", methods=['POST'])
def register():
    content = request.json
    user = User()
    response = user.add_user(content, database.get_connection())
    if response:
        return response
    else:
        if user.error:
            return "Malformed request", 400
        else:
            return "Data not found", 404

@app.route("/update_password", methods=['POST'])
def update_password():
    content = request.json
    user = User()
    response = user.update_password(content, database.get_connection())
    return response

@app.route("/api/add_system", methods=['POST'])
def add_system():       
    content = request.json
    system = System()
    response = system.add_system(content, database.get_connection())
    if response != None:
        return response
    else:
        if system.error:                
            return "Malformed JSON", 400
        else:                
            return "Data not found. Check log for more information", 500

@app.route("/api/update_system", methods=['POST'])
def update_system():       
    content = request.json
    system = System()
    response = system.update_system(content, database.get_connection())
    if response != None:
        return response
    else:
        if system.error:                
            return "Malformed JSON", 400
        else:                
            return "Data not found. Check log for more information", 500

@app.route("/api/get_systems", methods=['GET']) #Borrar 
def get_systems(): 
    system = System()      
    response = system.get_all_systems(database.get_connection())
    if response != None:
        return jsonify(response)
    else:
        if system.error:                
            return "Malformed JSON", 400
        else:                
            return "Data not found. Check log for more information", 500

# @socketio.on('connect')
# def init_connect():
#     # need visibility of the global thread object
#     global thread
#     print('Client connected')
#     #Start the random number generator thread only if the thread has not been started before.
#     if not thread.is_alive():
#         system = System()
#         systems = system.get_all_systems(database.get_connection())
#         number_transmition = 1
#         for system in systems:
#             for i in range(system["cameras"]):
#                 video_streaming = VideoStreaming(socketio, thread_stop_event, system, number_transmition, (i+1))
#                 video_streaming.set_database_manager(database.get_connection())              
#                 video_streaming.init_connection_to_ctv()
#                 video_streaming.init_model_detection()
#                 number_transmition = number_transmition + 1
#                 print("Starting Thread")
#                 thread = socketio.start_background_task(video_streaming.stream)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    print('Mensaje recibido: ' + data)

if __name__ == '__main__':
    database = Database()
    if(database.init_db()):
        socketio.run(app, host="0.0.0.0")
        database.close()