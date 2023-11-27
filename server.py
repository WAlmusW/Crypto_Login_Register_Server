from flask import Flask, request, jsonify
import base64

import auth
import crypto_utils
import post_get

app = Flask(__name__)


@app.route('/check_registration', methods=['POST'])
def check_registration():
    try:
        data = request.form
        device_udid = data.get('device_udid')
        print("device_udid: ", device_udid, type(device_udid))

        # Retrieve registration status from Firestore based on the device ID
        fs_client = auth.FirestoreClient()
        is_registered = fs_client.check_registration_status(device_udid)
        
        with open('public_key.pem', 'rb') as public_key_file:
            public_key = public_key_file.read()
            public_key_file.close()

        return jsonify({'is_registered': is_registered, 'public_key': public_key.decode('utf-8')})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.form
        encrypted_username = data.get('username')
        encrypted_password = data.get('password')
        encrypted_device_udid = data.get('device_udid')
        
        encrypted_username = base64.b64decode(encrypted_username)
        encrypted_password = base64.b64decode(encrypted_password)
        encrypted_device_udid = base64.b64decode(encrypted_device_udid)
        
        username = crypto_utils.decrypt_with_private_key(encrypted_username)
        password = crypto_utils.decrypt_with_private_key(encrypted_password)
        device_udid = crypto_utils.decrypt_with_private_key(encrypted_device_udid)
        
        fernet_key = crypto_utils.create_fernet_key(device_udid, username)
        
        # Check login status from Firestore based on the provided username and password
        fs_client = auth.FirestoreClient()
        is_logged_in = fs_client.check_login_status(username, password)

        return jsonify({'is_logged_in': is_logged_in, 'fernet_key': fernet_key.decode('utf-8')})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.form
        encrypted_username = data.get('username')
        encrypted_password = data.get('password')
        encrypted_device_udid = data.get('device_udid')
        encrypted_email = data.get('email')
        encrypted_phone_number = data.get('phone_number')
        
        print('debug1')
        
        encrypted_username = base64.b64decode(encrypted_username)
        encrypted_password = base64.b64decode(encrypted_password)
        encrypted_device_udid = base64.b64decode(encrypted_device_udid)
        encrypted_email = base64.b64decode(encrypted_email)
        encrypted_phone_number = base64.b64decode(encrypted_phone_number)
        
        print("debug 1.5")
        
        username = crypto_utils.decrypt_with_private_key(encrypted_username)
        password = crypto_utils.decrypt_with_private_key(encrypted_password)
        device_udid = crypto_utils.decrypt_with_private_key(encrypted_device_udid)
        email = crypto_utils.decrypt_with_private_key(encrypted_email)
        phone_number = crypto_utils.decrypt_with_private_key(encrypted_phone_number)
        
        print('debug2')
        
        fernet_key = crypto_utils.create_fernet_key(device_udid, username)
        
        print('debug3')
        
        # Register the user in Firestore based on the provided username and password
        fs_client = auth.FirestoreClient()
        fs_client.register_user(username, password, device_udid, email, phone_number)
        
        print('debug4')

        return jsonify({'message': 'User registered successfully', 'fernet_key': fernet_key.decode('utf-8')})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    
    
@app.route('/post_text', methods=['POST'])
def posting_text():
    try:
        data = request.form
        encrypted_title = data.get('title')
        encrypted_body = data.get('body')
        print("title: ", encrypted_title)
        print("body: ", encrypted_body)
        
        encrypted_title = base64.b64decode(encrypted_title)
        encrypted_body = base64.b64decode(encrypted_body)
        
        title = crypto_utils.decrypt_with_private_key(encrypted_title)
        body = crypto_utils.decrypt_with_private_key(encrypted_body)

        fs_client = post_get.FirestoreClient()
        fs_client.post_text(title, body)

        return jsonify({'message': "Text have been posted successfully"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    

@app.route('/get_text', methods=['POST'])
def getting_text():
    try:
        print("debug 0")
        data = request.form
        encrypted_title = data.get('title')
        encrypted_device_udid = data.get('device_udid')
        encrypted_username = data.get('username')
        
        print("debug 1")
        
        encrypted_title = base64.b64decode(encrypted_title)
        encrypted_device_udid = base64.b64decode(encrypted_device_udid)
        encrypted_username = base64.b64decode(encrypted_username)
        
        print("debug 2")
        
        title = crypto_utils.decrypt_with_private_key(encrypted_title)
        device_udid = crypto_utils.decrypt_with_private_key(encrypted_device_udid)
        username = crypto_utils.decrypt_with_private_key(encrypted_username)
        
        print("debug 3")

        fs_client = post_get.FirestoreClient()
        text_map = fs_client.get_text(title)
        
        title_from_map = text_map.get('Title')
        body_from_map = text_map.get('Body')
        
        encrypted_title = crypto_utils.encrypt_with_fernet_key(title_from_map, device_udid, username)
        encrypted_body = crypto_utils.encrypt_with_fernet_key(body_from_map, device_udid, username)
        
        return jsonify({'message': "Text have been posted successfully", 'encrypted_title': encrypted_title, 'encrypted_body': encrypted_body})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    crypto_utils.generate_rsa_key_pair()
    app.run(host='0.0.0.0', port=5000)  # You can choose a different port if needed
