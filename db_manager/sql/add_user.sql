INSERT INTO users (username, email, password) 
VALUES (%s, %s, %s) RETURNING *;