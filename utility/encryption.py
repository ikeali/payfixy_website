from cryptography.fernet import Fernet
from decouple import config

key = config('SECRET_ENCRYPTION_KEY') 
fernet = Fernet(key)

def encrypt_data(data):
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    return fernet.decrypt(encrypted_data.encode()).decode()
