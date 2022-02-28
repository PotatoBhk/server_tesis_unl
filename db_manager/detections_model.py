from psycopg2 import DatabaseError
from flask import jsonify
import os

class Detection():
    
    def __init__(self):
        root = os.path.dirname(__file__)
        self.sql_folder = os.path.realpath(os.path.join(root, "sql"))
        self.error = False
        print("Detection class initialized")
        
    def add_detection(self, json, db_manager):
        if not self._json_to_data(json):        
            add_detection = os.path.join(self.sql_folder, "add_detection.sql")
            with open(add_detection, 'r') as f:
                sql_add_detection = f.read()
            
            try:            
                cur = db_manager.cursor()
                cur.execute(sql_add_detection, (
                        self.system,
                        self.camera,
                        self.model,
                        self.detection_time,
                        self.image,
                        self.movement,
                        self.person
                    )
                )
                system = cur.fetchone()
                self._serialize(system)
                db_manager.commit()    
                cur.close()
                return self._data_to_json()
            except DatabaseError as error:
                print("Error en la base de datos: ", error)
                return None
        else:
            return None
        
    def _serialize(self, data):
        self.id = data[0]
        self.system = data[1]
        self.camera = data[2]
        self.model = data[3]
        self.detection_time = data[4]
        self.image = data[5]
        self.movement = data[6]
        self.person = data[7]        
    
    def _json_to_data(self, json):
        try:
            self.id = json["id"]
            self.system = json["system"]
            self.camera = json["camera"]
            self.model = json["model"]
            self.detection_time = json["detection_time"]
            self.image = json["image"]
            self.movement = json["movement"]
            self.person = json["person"]            
        except KeyError as err:
            print("Error en _json_to_data: ", err)
            self.error = True
    
    def _data_to_json(self):
        return jsonify({
            "id": self.id,
            "cameras": self.cameras,
            "link": self.link,
            "model": self.model
        })