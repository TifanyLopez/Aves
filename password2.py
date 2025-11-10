# werkzeug
from werkzeug.security import generate_password_hash, check_password_hash

texto = "x?_ph"
# Contraseña encriptada: ejecuta con "py password2.py" y luego verifica la comparación
texto_encriptado = generate_password_hash(texto)
print(f"Texto encriptado: {texto_encriptado}")

# Verificar si el texto es correcto
print(f"¿El texto correcto? {check_password_hash(texto_encriptado, texto)}")

