"""Schema for user"""
from pydantic import BaseModel

class userRegister(BaseModel):
    username: str
    password: str

class userLogin(BaseModel):
    username: str
    password: str
