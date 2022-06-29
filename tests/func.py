import bcrypt
password = "123456"
print(password.encode('utf-8'))
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed)
print(hashed.decode('utf-8'))