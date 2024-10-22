from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    uid: str
    email: str
    user_name: Optional[str] = None
    gender: Optional[str] = None 
    token: Optional[str] = None  # Make token optional