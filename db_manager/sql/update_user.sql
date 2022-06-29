UPDATE users
SET password = %s
WHERE username = %s 
RETURNING *;