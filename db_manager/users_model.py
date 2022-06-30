from psycopg2 import DatabaseError
from flask import jsonify
import bcrypt
import os


class User():
    
    def __init__(self):
        root = os.path.dirname(__file__)
        self.sql_folder = os.path.realpath(os.path.join(root, "sql"))
        print("User class initialized")
    
    def add_user(self, json, db_manager):
        if not self._json_to_data(json):        
            add_user = os.path.join(self.sql_folder, "add_user.sql")
            with open(add_user, 'r') as f:
                sql_add_user = f.read()
            
            try:
                cur = db_manager.cursor()
                hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
                cur.execute(sql_add_user, (self.username, self.email, hashed.decode('utf-8')))
                user = cur.fetchone()
                self._serialize(user)
                db_manager.commit()    
                cur.close()
                return self._data_to_json()
            except DatabaseError as error:
                print("Error en la base de datos: ", error)
                return None
        else:
            return None
    
    def update_password(self, json, db_manager):
        username = json['username']
        newpassword = json['newpassword']
        oldpassword = json['oldpassword']
        
        update_user = os.path.join(self.sql_folder, "update_user.sql")
        with open(update_user, 'r') as f:
            sql_update_user = f.read()
        
        get_user = os.path.join(self.sql_folder, "get_user.sql")
        with open(get_user, 'r') as f:
            sql_get_user = f.read()
        
        try:
            cur = db_manager.cursor()
            sql_get_user = sql_get_user.replace("%s", username)
            cur.execute(sql_get_user)
            chk_user = cur.fetchone()       
            is_valid = bcrypt.checkpw(oldpassword.encode('utf-8'), chk_user[1].encode('utf-8'))
            
            if not is_valid:
                return jsonify({
                    'status': True,
                    'isError': False,
                    'isValid': is_valid,
                    'message': 'Password incorrect'
                })
                
            hashed = bcrypt.hashpw(newpassword.encode('utf-8'), bcrypt.gensalt())
            cur.execute(sql_update_user, (hashed.decode('utf-8'), username))
            user_updated = cur.fetchone()
            user_id = user_updated[0]            
            db_manager.commit()    
            cur.close()
            if user_id > 0:
                return jsonify({
                    'status': True,
                    'isError': False,
                    'isValid': is_valid,
                    'message': 'Password updated'
                })
            else:
                return jsonify({
                    'status': False,
                    'isError': True,
                    'isValid': is_valid,
                    'message': 'Password not updated, SQL error'
                })
        except DatabaseError as error:
            print("Error en la base de datos: ", error)
            return jsonify({
                'status': False,
                'isError': True,
                'isValid': False,
                'message': 'Password not updated, SQL error'
            })
    
    def validate_user(self, json, db_manager):
        if not self._json_to_data(json):
            get_user = os.path.join(self.sql_folder, "get_user.sql")
            with open(get_user, 'r') as f:
                sql_get_user = f.read()
            
            try:
                cur = db_manager.cursor()
                sql_get_user = sql_get_user.replace("%s", self.username)
                cur.execute(sql_get_user)
                result = cur.fetchone()
                cur.close()                
                pwd = result[1].encode('utf-8')
                password = self.password.encode('utf-8')                
                check = bcrypt.checkpw(password, pwd)
                return jsonify({
                    'status': True,
                    'isValid': check,
                    'message': 'User validated'
                })
            except DatabaseError as error:
                print("Error en la base de datos: ", error)
                return jsonify({
                    'status': False,
                    'isValid': False,
                    'message': 'Database error'
                }) 
        else:
            return jsonify({
                'status': False,
                'isValid': False,
                'message': 'Error when deserializing JSON'
            })
    
    def _serialize(self, user):
        self.id = user[0]
        self.username = user[1]
        self.email = user[2]
        self.password = user[3]
        
    def _json_to_data(self, json):
        try:
            self.id = json['id']
            self.username = json['username']
            self.email = json['email']
            self.password = json['password']
        except KeyError as err:
            print("Error en _json_to_data: ", err)
            self.error = True
    
    def _data_to_json(self):
        return jsonify({
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        })