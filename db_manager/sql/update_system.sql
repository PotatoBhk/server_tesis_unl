UPDATE systems
SET name = %s, cameras = %s, link = %s, model = %s
WHERE id = %s
RETURNING *;