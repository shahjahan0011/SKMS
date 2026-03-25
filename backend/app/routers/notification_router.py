"""endpoints for notifications"""
from fastapi import APIRouter, HTTPException, Query, Depends

from app.services.notification_service import NotificationService
from app.services.auth_service import AuthService
from app.storage.repositories.user_repository import UserRepository
from app.dependencies import (
    get_notification_service,
    get_auth_service,
    get_user_repository
)
from app.constants import HTTPStatusCode, UserRole, ErrorMessages

router = APIRouter(prefix="/Notifications", tags=["Notifications"])


@router.get("/")
def get_user_notifications(
    username: str = Query(...),
    user_repo: UserRepository = Depends(get_user_repository),  
    service: NotificationService = Depends(get_notification_service)  
):
    """return notifications for a specific user"""
    
    user = user_repo.get_user_by_username(username)

    if user is None:
        raise HTTPException(
            status_code=HTTPStatusCode.NOT_FOUND,
            detail=ErrorMessages.USER_NOT_FOUND
        )

    notifications = service.get_user_notifications(username)

    return {
        "username": username,
        "notifications": notifications
    }


@router.get("/role")
def get_role_notifications(
    role: str = Query(...),
    username: str = Query(...),
    auth: AuthService = Depends(get_auth_service), 
    service: NotificationService = Depends(get_notification_service)  
):
    """allow admin users to view notifications by role"""

    try:
        auth.check_role(username, UserRole.ADMIN.value)
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

    notifications = service.get_role_notifications(role)

    return {
        "role": role,
        "notifications": notifications
    }
