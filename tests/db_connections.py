import psycopg2
import os

root = os.path.dirname(__file__)
sql_folder = os.path.realpath(os.path.join(root, "..", "db_manager/sql"))
schema = os.path.join(sql_folder, "schema.sql")
add_system = os.path.join(sql_folder, "add_system.sql")

with open(schema, 'r') as f:
    sql_schema = f.read()

with open(add_system, 'r') as f:
    sql_add_system = f.read()

try:
    conn = psycopg2.connect(
        user = 'cieyttesis', 
        password = 'mpassword',
        database = 'unlobjdet'
    )
    print('Connected')
        
    cur = conn.cursor()
    cur.execute(sql_schema)
    print(sql_add_system)   
    cur.execute(sql_add_system, (3,"TestLink2","YOLOv4"))
    system = cur.fetchone()
    print(system)
    
    conn.commit()    
    cur.close() 
    conn.close()
except psycopg2.DatabaseError as error:
    print("Error en la base de datos: ", error)