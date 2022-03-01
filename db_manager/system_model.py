from psycopg2 import DatabaseError
from flask import jsonify
import os

class System():
    
    def __init__(self):
        root = os.path.dirname(__file__)
        self.sql_folder = os.path.realpath(os.path.join(root, "sql"))        
        self.error = False
        print("System class initialized")
        
    def add_system(self, json, db_manager):
        if not self._json_to_data(json):        
            add_system = os.path.join(self.sql_folder, "add_system.sql")
            with open(add_system, 'r') as f:
                sql_add_system = f.read()
            
            try:            
                cur = db_manager.cursor()
                cur.execute(sql_add_system, (self.cameras,self.link,self.model))
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
    
    def update_system(self, json, db_manager):
        if not self._json_to_data(json):        
            update_system = os.path.join(self.sql_folder, "update_system.sql")
            with open(update_system, 'r') as f:
                sql_update_system = f.read()
            
            try:            
                cur = db_manager.cursor()
                cur.execute(sql_update_system, (self.cameras,self.link,self.model, self.id))
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
    
    def get_all_systems(self, db_manager):
        list_systems = os.path.join(self.sql_folder, "list_system.sql")
        with open(list_systems, 'r') as f:
            sql_list_systems = f.read()
            
        try:
            cur = db_manager.cursor()
            cur.execute(sql_list_systems)
            systems = cur.fetchall()
            cur.close()
            
            systems_json = list()
            for system in systems:
                self._serialize(system)
                systems_json.append(self._data_to_json())
            return systems_json
        except DatabaseError as error:
            print("Error en la base de datos: ", error)
            return None
        
    def _serialize(self, data):
        self.id = data[0]
        self.cameras = data[1]
        self.link = data[2]
        self.model = data[3]
    
    def _json_to_data(self, json):
        try:
            self.id = json["id"]
            self.cameras = json["cameras"]
            self.link = json["link"]
            self.model = json["model"]
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
        
    def get_id(self):
        return self.id
    
    def get_cameras(self):
        return self.cameras
    
    def get_link(self):
        return self.link
    
    def get_model(self):
        return self.model
    
    # def set_id(self, id):
    #     self.id = id
    
    # def set_cameras(self, cameras):
    #     self.cameras = cameras
    
    # def set_link(self, link):
    #     self.link = link
    
    # def set_model(self, model):
    #     self.model = model