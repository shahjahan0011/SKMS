"""Schema for user"""
from typing import Optional

from pydantic import BaseModel


class UserRegister(BaseModel):
    """schema used when a user registers an account"""

    username: str
    password: str
    role: Optional[str] = "user"


class UserLogin(BaseModel):
    """schema used when a user logs in"""

    username: str
    password: str


class UserResponse(BaseModel):
    """schema returned to the client without exposing sensitive data"""

    username: str
    role: str
