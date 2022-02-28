INSERT INTO systems (cameras, link, model) 
VALUES (%s, %s, %s) RETURNING *;