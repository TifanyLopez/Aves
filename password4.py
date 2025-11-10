from cryptography.fernet import Fernet 

texto = "x?_ph" 

clave = Fernet.generate_key()
objeto = Fernet(clave)

# Encriptar
texto_encriptado = objeto.encrypt(texto.encode())   
print(f"Texto encriptado: {texto_encriptado}")

# Desencriptar el texto
texto_desencriptado = objeto.decrypt(texto_encriptado).decode()
print(f"Texto desencriptado: {texto_desencriptado}")
    
        
                                         