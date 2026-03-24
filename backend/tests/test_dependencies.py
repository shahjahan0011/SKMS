"""Tests for dependency injection"""
from unittest.mock import Mock

from app.dependencies import (
    get_auth_service,
    get_notification_service,
    get_user_repository,
    get_notification_repository
)
from app.services.auth_service import AuthService
from app.services.notification_service import NotificationService
from app.storage.repositories.user_repository import UserRepository
from app.storage.repositories.notification_repository import NotificationRepository


def test_get_auth_service_returns_instance():
    """test auth service dependency returns correct instance"""
    service = get_auth_service()
    assert isinstance(service, AuthService)


def test_get_notification_service_returns_instance():
    """test notification service dependency returns correct instance"""
    service = get_notification_service()
    assert isinstance(service, NotificationService)


def test_get_user_repository_returns_instance():
    """test user repository dependency returns correct instance"""
    repo = get_user_repository()
    assert isinstance(repo, UserRepository)


def test_get_notification_repository_returns_instance():
    """test notification repository dependency returns correct instance"""
    repo = get_notification_repository()
    assert isinstance(repo, NotificationRepository)


def test_auth_service_accepts_repository_injection():
    """test auth service can accept injected repository"""
    
    mock_repo = Mock(spec=UserRepository)
    service = AuthService(user_repo=mock_repo)
    
    assert service.user_repo == mock_repo


def test_notification_service_accepts_repository_injection():
    """test notification service can accept injected repository"""
    
    mock_repo = Mock(spec=NotificationRepository)
    service = NotificationService(notification_repo=mock_repo)
    
    assert service.notification_repo == mock_repo


def test_dependencies_are_independent():
    """test each dependency call creates new instance"""
    
    service1 = get_auth_service()
    service2 = get_auth_service()
    
    assert service1 is not service2