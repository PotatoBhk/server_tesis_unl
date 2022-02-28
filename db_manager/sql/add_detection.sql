INSERT INTO detections (system, camera, model, detection_time, image, movement, person) 
VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;