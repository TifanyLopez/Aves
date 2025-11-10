from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)   # py password1.py para ver si se creó   
bcrypt = Bcrypt(app)

# Generar hash de una contraseña
password_plano = "contraseña_secreta"
hash_password = bcrypt.generate_password_hash(password_plano).decode('utf-8')
print("Contraseña encriptada:", hash_password)

# Verificar la contraseña
contraseña_interna = "contraseña_secreta"
verificacion = bcrypt.check_password_hash(hash_password, contraseña_interna)
print(f"¿Contraseña correcta? {verificacion}")

