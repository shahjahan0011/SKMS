"""endpooints for the fastapi"""
from fastapi import APIRouter, HTTPException, Query, Depends

from app.schemas.user_schema import user_login, user_register
from app.services.auth_service import auth_service
from app.constants import HTTPStatusCode, UserRole
from app.dependencies import get_auth_service

router = APIRouter()


@router.post("/register")
def register(
    user: user_register,
    service: auth_service = Depends(get_auth_service) 
):
    """register a new user"""

    try:
        created_user = service.register_user(
            user.username,
            user.password,
            user.role
        )
        return created_user
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPException.BAD_REQUEST, 
            detail=str(error)
        ) from error


@router.post("/login")
def login(
    user: user_login,
    service: auth_service = Depends(get_auth_service)  
):
    """log in an existing user"""

    try:
        logged_in_user = service.login_user(
            user.username,
            user.password
        )
        return logged_in_user
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatusCode.UNAUTHORIZED, 
            detail=str(error)
        ) from error


@router.post("/logout")
def logout():
    """log out the current user"""

    return {"message": "logout successful"}

@router.get("/admin")
def admin_access(
    username: str = Query(...),
    service: auth_service = Depends(get_auth_service)  # DEPENDENCY INJECTION
):
    """allow access only to admin users"""
  
    try:
        service.check_role(username, UserRole.ADMIN.value)
        return {"message": "admin access granted"}
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatusCode.NOT_FOUND,
            detail=str(error)
        ) from error
    except PermissionError as error:
        raise HTTPException(
            status_code=HTTPStatusCode.FORBIDDEN,
            detail=str(error)
        ) from error
