INSERT INTO systems (name, cameras, link, model) 
VALUES (%s, %s, %s, %s) RETURNING *;