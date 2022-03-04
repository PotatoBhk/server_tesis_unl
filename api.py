from flask import Flask, request, jsonify
from db_manager.system_model import  System
from db_manager.database import Database

app = Flask(__name__)

database = None

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

if __name__ == '__main__':
    database = Database()
    if(database.init_db()):
        app.run(port = 3000)