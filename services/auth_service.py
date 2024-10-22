from firebase_admin import auth, firestore  # Import firestore module
from models.user_model import User
from firebase.firebase_init import db  # Firestore client
from typing import Optional

class AuthService:
    def signup(self, email: str, password: str, user_name: Optional[str] = None, gender: Optional[str] = None) -> User:
        # Create a new user with Firebase Authentication
        user_record = auth.create_user(email=email, password=password)

        # Prepare user data for Firestore
        user_data = {
            "uid": user_record.uid,
            "email": user_record.email,
            "user_name": user_name if user_name else None,  # Use user_name if provided
            "gender": gender,  # Store gender in Firestore
            "created_at": firestore.SERVER_TIMESTAMP  # Automatically set the timestamp
        }

        # Add the user to Firestore
        db.collection("users").document(user_record.uid).set(user_data)

        return User(uid=user_record.uid, email=user_record.email, user_name=user_name, gender=gender)
    
    def login(self, email: str, password: str) -> User:
        # Login verification (typically done on the client-side, but token verification can be done here)
        user = auth.get_user_by_email(email)
        token = self.get_token(user.uid)  # Generate or retrieve a token
        return User(uid=user.uid, email=user.email, token=token)

    def get_token(self, uid: str):
        """This is a utility function to generate tokens if needed."""
        return auth.create_custom_token(uid)
    
    def google_login(self, id_token: str) -> User:
        """
        Verifies Google ID Token and either signs up or logs in the user.
        """
        try:
            # Verify the ID token from Google
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token['email']
            user_name = decoded_token.get('name')  # Retrieve user name from the Google account if available
            gender = decoded_token.get('gender')  # Retrieve gender from the Google account if available

            # Check if the user already exists in Firestore
            user_ref = db.collection("users").document(uid)
            user_data = user_ref.get()
            if user_data.exists:
                # User exists, return their data
                user_data = user_data.to_dict()
                return User(uid=uid, email=email, user_name=user_data.get('user_name'), gender=user_data.get('gender'))

            # User does not exist, create a new record in Firestore
            user_data = {
                "uid": uid,
                "email": email,
                "user_name": user_name,  # This user_name comes from Google
                "gender": gender,  # Store gender if provided by Google
                "created_at": firestore.SERVER_TIMESTAMP
            }
            user_ref.set(user_data)

            # Return the new user data
            return User(uid=uid, email=email, user_name=user_name, gender=gender)

        except Exception as e:
            raise Exception(f"Error during Google login: {str(e)}")