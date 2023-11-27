import os
import rsa
import base64
from cryptography.fernet import Fernet
import hashlib

def generate_rsa_key_pair():
    if not os.path.exists('private_key.pem'):
        print("Creating Public and Private RSA Key pair...")
        (public_key, private_key) = rsa.newkeys(4096, poolsize=8)
        
        with open('private_key.pem', mode='wb') as private_key_file:
            byte_private_key = private_key.save_pkcs1()
            private_key_file.write(byte_private_key)
            private_key_file.close()
            
        with open('public_key.pem', mode='wb') as public_key_file:
            byte_public_key = public_key.save_pkcs1()
            public_key_file.write(byte_public_key)
            public_key_file.close()
        
        print("Public and Private RSA Key pair is saved")


def decrypt_with_private_key(encrypted_message):
    print("Decrypting message with private key")
    with open('private_key.pem', 'rb') as private_key_file:
        print("debug 1")
        private_key = private_key_file.read()
        RSA_private_key = rsa.PrivateKey.load_pkcs1(private_key)
        print("debug 2")
        private_key_file.close()
    
    print("debug 3")
    decrypted_bytes = rsa.decrypt(encrypted_message, RSA_private_key)
    decrypted_string = decrypted_bytes.decode('utf-8')
    print("Decryption successful")
    return decrypted_string


def create_fernet_key(device_id, username):
    print("Creating fernet key...")
    # Combine device ID and username
    combined_data = f"{device_id}:{username}".encode()

    # Hash the combined data using SHA256
    fernet_key_bytes = hashlib.sha256(combined_data).digest()
    fernet_key = base64.b64encode(fernet_key_bytes)
    
    with open('fernet_key.pem', mode='wb') as fernet_key_file:
            fernet_key_file.write(fernet_key)
            fernet_key_file.close()
    
    print("Fernet key is saved")
    return fernet_key


def encrypt_with_fernet_key(message, device_udid, username):
    key = device_udid + username
    fernetKey = Fernet(base64.b64encode(hashlib.sha256(key.encode()).digest()))
    cipher = fernetKey.encrypt(message.encode())
    return base64.b64encode(cipher).decode('ascii')
