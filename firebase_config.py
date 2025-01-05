import firebase_admin
from firebase_admin import credentials

# Initialize Firebase Admin SDK
def initialize_firebase():
    #Initializing DB
    cred = credentials.Certificate("db_encrypted_key.json")
    firebase_admin.initialize_app(cred)
    print("Firebase initialized")

    