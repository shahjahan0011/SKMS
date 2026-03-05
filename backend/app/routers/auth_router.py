"""Endpoint creater for user"""
from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import userRegister, userLogin
from app.services.auth_service import register_user, login_user

router = APIRouter()

@router.post("/register")
def register(user: userRegister):
    register_user(user.username, user.password)
    return {"message": "User registered"}

@router.post("/login")
def login(user: userLogin):
    success = login_user(user.username, user.password)

    if not success:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}
