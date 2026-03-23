"""endpoints for notifications"""
from fastapi import APIRouter, HTTPException, Query

from app.services.notification_service import notification_service
from app.services.auth_service import auth_service
from app.storage.repositories.user_repository import user_repository
from app.constants import HTTPStatusCode, UserRole, ErrorMessages

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/")
def get_user_notifications(username: str = Query(...)):
    """return notifications for a specific user"""

    user_repo = user_repository()
    user = user_repo.get_user_by_username(username)

    if user is None:
        raise HTTPException(status_code=HTTPStatusCode.NOT_FOUND, detail=ErrorMessages.USER_NOT_FOUND)

    service = notification_service()
    notifications = service.get_user_notifications(username)

    return {
        "username": username,
        "notifications": notifications
    }


@router.get("/role")
def get_role_notifications(
    role: str = Query(...),
    username: str = Query(...)
):
    """allow admin users to view notifications by role"""

    auth = auth_service()

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
 
    service = notification_service()
    notifications = service.get_role_notifications(role)
 
    return {
        "role": role,
        "notifications": notifications
    }
