"""Schema for user"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class user_register(BaseModel):
    """schema used when a user registers an account"""

    email: EmailStr
    password: str
    role: Optional[str] = "user"


class user_login(BaseModel):
    """schema used when a user attempts to log in"""

    email: EmailStr
    password: str


class user_response(BaseModel):
    """schema returned to the client without exposing sensitive data"""

    email: EmailStr
    role: str
