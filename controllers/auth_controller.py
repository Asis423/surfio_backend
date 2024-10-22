from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.auth_service import AuthService
from utils.validation import validate_signup
from typing import Optional

router = APIRouter()

# Request body models for signup and login
class UserSignup(BaseModel):
    email: str
    password: str
    user_name: Optional[str] = None  # Added user_name field
    gender: str  # Add gender field

class UserLogin(BaseModel):
    email: str
    password: str

class GoogleLogin(BaseModel):
    id_token: str

# AuthService dependency
auth_service = AuthService()

@router.post("/signup")
async def signup(user: UserSignup):
    validate_signup(user.email, user.password)  # Validation
    try:
        user_data = auth_service.signup(user.email, user.password, user.user_name, user.gender)  # Pass gender to the service
        return {"message": "User created successfully", "user": user_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user: UserLogin):
    try:
        user_data = auth_service.login(user.email, user.password)
        return {"message": "Login successful", "user": user_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/google-login")
async def google_login(google_data: GoogleLogin):
    """
    Log in or sign up a user using Google ID Token.
    """
    try:
        user_data = auth_service.google_login(google_data.id_token)
        return {"message": "Login successful", "user": user_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))