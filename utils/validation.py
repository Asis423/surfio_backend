import re
from fastapi import HTTPException

def validate_signup(email: str, password: str):
    # Check email validity
    if not re.match(r"[^@]+@[^@]+.[^@]+", email):
        raise HTTPException(status_code=400, detail="Invalid email format")

# Check password strength (e.g., minimum 6 characters)
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")

def validate_login(email: str, password: str):
    # Reuse the same email validation for login
    if not re.match(r"[^@]+@[^@]+.[^@]+", email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    if not password:
        raise HTTPException(status_code=400, detail="Password cannot be empty")