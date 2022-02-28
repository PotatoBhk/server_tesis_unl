UPDATE systems
SET cameras = %s, link = %s, model = %s
WHERE id = %s
RETURNING *;