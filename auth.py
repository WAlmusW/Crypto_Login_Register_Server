import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Replace these Firestore configuration values with your own
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "loginregister-25083",
    "private_key_id": "de8f3bbfc89664d75630c2e489e085588ba25c3b",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCLTC7V2yB4yb0+\neBDV7ORXCtVvfxsMGWSOELDme0tWntxlsPrnBKl9m8uLNhZCY/dAwhaLJNvqOIb3\nO0ys8deK2azlsl155cxr2/4n7FHlAwWRto1k1OUVss7wnFx1KXKNpzl3T5+u2ftQ\nhjFNqpxSBhoAHuyYLAZWX3PxIAO+FcCjo7VmsdFNmdjhtECLi2qQxJih0VMl7qt3\niNZjyOn731Z4khr6C0lmRW1WHS+N8m1DQePI6nOul0W2zwxYFiYfQFI2qXQYrbP+\nAGZt6JNXJxIgeRtqJKcBa5LXXAlH+CbpR1GNvlLD2bRgJr7FZqW4sgzgzRgjqRbQ\nanW1FwA1AgMBAAECggEAP6AMEn103wcSrApucjAyefmGVNejVIryrZs9GgF9/3Iv\nbDmC2Ot9uVRki9EoKKn9gTRF1MeAtYKdTybkVmhekdrsSLyISsnmbeu9sqGUJH0V\nWaGfAsvlWVxjfm6FIrTMUJxtuKwDXXvOeVDaC0YfAa4syRpW6gjN2jzeOehsHTGo\nyu3z1GLyt6sdxMKyeeQ4Da3XEZmeESnPqQP9R+DQkn7T6hMPDb6xjeHsF9CQtkK3\nISARQoxQ/3umnJqxtsMcrJnhc2BUCGtZE2Pq8bhug7Hl2tzbiUZvMmrqje3o8/rE\n6S4SUVUlxFKqJ0rishEsF0G3jOlg8xInxaOyPYohXwKBgQDB0+GUpbzD962DGhA1\n0Os4rVpQeCKT8wLBhiC1X5ruXDG7xoiD8GNidDGY8lUoBIdyZdcsaD0+uDWwHqx9\nqq8fLm7eae4jUNv8AQyeqgJMoYRmJfVe6fkPp2fUJXFnSGX8wC1YYGxNpphmgJc/\nk7QzrZ5gBONxMGV5hFm4cpDv6wKBgQC3+pN7q+ZaxeZ5JLiaai396y5pVRC5y8Fm\nKHeyAy64A2HuwQMi65bUa9uz+twXm4TSHbAR3YxMYkFByE5KIQ6WS8+gRJk3F6yx\nXebx99u4lSjyRzG/xmMDQf/nwSXguVTZBho/PXrNu1Ogh14eH//zcbuEvqgqlmFA\ntNG1MGPoXwKBgAPCTzKp0DJgwE21mLDif11XB1ReMBV8dgY4yrOZyhBrW0+P9x/P\n7q1/IWMc+AfRpqrSTM0ArIdl3SywO5ooUEMjjGTl2wd2Tv3hK1R8aZUA4Od2Pv77\nPKhQD9RucXeWUNwJAhgfrpoG7Be40LYb8De8W0Dzd1G/pYgox/Cq0CLHAoGADlYt\ndf6wRbSUQC53YDkT+myAQl8JnaDeIkrXAP00f8xrrkJGL0tyhn0dMspCqmhJEmKT\n3OCJ1U32zdyBFU+8JkQkGtYdpmhm4a9ylrp82cZt2Wto2gvonVFgUrv/aqKmlP7f\nvrvYvP1zB9hkoi5WMK9VMIP28NKlI3izus3ZizsCgYEAnph6YeJe5es/mJbTpMkm\nnhzyY1JMD7PkZFYnay8/DsQism3vXpVfYJJu6n7fQSwhAV4tr2SspEfZE57doJmt\nhfJ6LUQGrptevQX5gwIseenjgo26WKXWE64AUiIjttdY2C9ADMoXlGPE+BI0N0PS\nUIeo4BVSk8uyHyfDcKy7Z0A=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ui050@loginregister-25083.iam.gserviceaccount.com",
    "client_id": "113954095505981934090",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ui050%40loginregister-25083.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
})

firebase_admin.initialize_app(cred)
db = firestore.client()

class FirestoreClient:
    def check_registration_status(self, device_udid):
        # Query the "users" collection for documents where "Device_ID" is equal to device_udid
        query = db.collection('users').where('Device_ID', '==', device_udid)
        documents = query.get()

        # Check if there are any matching documents
        is_registered = len(documents) > 0

        return is_registered
    
    
    def check_login_status(self, username, password):
        # Reference to the "users" collection in Firestore
        users_ref = db.collection('users')

        # Query to check if the provided username and password match any documents
        documents = users_ref.get()

        # Check if any documents match the query
        is_logged_in = False
        for document in documents:
            user_username = document.get('Username')
            user_password = document.get('Password')

            # If the device ID matches, consider it registered
            if username == user_username and password == user_password:
                is_logged_in = True
                print("debug check")
                break  # No need to continue checking

        return is_logged_in
    
    
    def register_user(self, username, password, device_udid, email, phone_number):
        try:
            users_ref = db.collection('users')

            users_ref.document(username).set({
                'Device_ID': device_udid,
                'Username': username,
                'Password': password,
                'Email': email,
                'Phone_Number': phone_number,
            })

            print(username, password, device_udid)
            print('User registered successfully')
        except Exception as e:
            print(f'Error registering user: {e}')