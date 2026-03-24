"""Dependency injection for FastAPI"""
from app.services.auth_service import AuthService
from app.services.notification_service import NotificationService
from app.storage.repositories.user_repository import UserRepository
from app.storage.repositories.notification_repository import NotificationRepository
 
 
def get_auth_service() -> AuthService:
    """Dependency that provides auth_service instance"""
    return AuthService()
 
 
def get_notification_service() -> NotificationService:
    """Dependency that provides notification_service instance"""
    return NotificationService()
 
 
def get_user_repository() -> UserRepository:
    """Dependency that provides user_repository instance"""
    return UserRepository()
 
 
def get_notification_repository() -> NotificationRepository:
    """Dependency that provides notification_repository instance"""
    return NotificationRepository()
