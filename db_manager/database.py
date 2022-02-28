import psycopg2
import os

class Database():
    
    def __init__(self):
        root = os.path.dirname(__file__)
        self.sql_folder = os.path.realpath(os.path.join(root, "sql"))
        print("Database class initialized")
        
    def init_db(self):
        try:
            #Read Schema's SQL file
            schema = os.path.join(self.sql_folder, "schema.sql")
            with open(schema, 'r') as f:
                sql_schema = f.read()
            #Initiate and connect with database   
            self.conn = psycopg2.connect(
                user = 'cieyttesis', 
                password = 'mpassword',
                database = 'unlobjdet'
            )
            cur = self.conn.cursor()
            cur.execute(sql_schema)
            self.conn.commit()
            cur.close()                        
            return True
        except psycopg2.DatabaseError as error:
            print("Error en la base de datos: ", error)
            self.conn.close()
            return False
    
    def get_connection(self):
        return self.conn
    
    def close(self):
        try:
            self.conn.close()
            print("Conexión con base de datos terminada...")
        except psycopg2.DatabaseError as error:
            print("Error al cerrar la conexión de la BDD: ", error)