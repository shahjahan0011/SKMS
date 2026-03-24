"""Dependency injection for FastAPI"""
from app.services.auth_service import auth_service
from app.services.notification_service import notification_service
from app.storage.repositories.user_repository import user_repository
from app.storage.repositories.notification_repository import notification_repository
 
 
# Service Dependencies
def get_auth_service() -> auth_service:
    """Dependency that provides auth_service instance"""
    return auth_service()
 
 
def get_notification_service() -> notification_service:
    """Dependency that provides notification_service instance"""
    return notification_service()
 
 
# Repository Dependencies
def get_user_repository() -> user_repository:
    """Dependency that provides user_repository instance"""
    return user_repository()
 
 
def get_notification_repository() -> notification_repository:
    """Dependency that provides notification_repository instance"""
    return notification_repository()
