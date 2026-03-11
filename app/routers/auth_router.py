"""endpooints for the fastapi"""
from fastapi import APIRouter, HTTPException

from app.schemas.user_schema import user_login, user_register
from app.services.auth_service import auth_service

router = APIRouter()


@router.post("/register")
def register(user: user_register):
    """register a new user"""

    service = auth_service()

    try:
        created_user = service.register_user(
            user.username,
            user.password,
            user.role
        )
        return created_user
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/login")
def login(user: user_login):
    """log in an existing user"""

    service = auth_service()

    try:
        logged_in_user = service.login_user(
            user.username,
            user.password
        )
        return logged_in_user
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error


@router.post("/logout")
def logout():
    """log out the current user"""

    return {"message": "logout successful"}
