import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app
cred = credentials.Certificate('E:/SURFIO/surfio-417b9-firebase-adminsdk-vp4nr-41c65a03aa.json')
firebase_app = firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()