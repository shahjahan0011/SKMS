"""endpoint testing for notification router"""
from unittest.mock import Mock
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_user_repository, get_notification_service, get_auth_service
from app.constants import HTTPStatusCode, UserRole, NotificationEventType, ErrorMessages
from app.services.auth_service import AuthService

client = TestClient(app)


def test_get_user_notifications():
    """test user notification retrieval endpoint"""

    mock_user_repo = Mock()
    mock_user_repo.get_user_by_username.return_value = {
        "username": "jahan",
        "role": UserRole.USER.value
    }

    mock_notification_service = Mock()
    mock_notification_service.get_user_notifications.return_value = [
        {
            "id": "n1",
            "user_id": "jahan",
            "role": UserRole.CUSTOMER.value,
            "event_type": NotificationEventType.ORDER_CREATED.value,
            "event_key": f"{NotificationEventType.ORDER_CREATED.value}:101:jahan",
            "message": "Your order 101 was created successfully.",
            "order_id": "101",
            "created_at": "2026-03-21T12:00:00+00:00"
        }
    ]

    app.dependency_overrides[get_user_repository] = lambda: mock_user_repo
    app.dependency_overrides[get_notification_service] = lambda: mock_notification_service

    try:
        response = client.get("/Notifications/?username=jahan")

        assert response.status_code == HTTPStatusCode.OK
        assert response.json()["username"] == "jahan"
        assert len(response.json()["notifications"]) == 1
        assert response.json()["notifications"][0]["user_id"] == "jahan"

        mock_user_repo.get_user_by_username.assert_called_once_with("jahan")
        mock_notification_service.get_user_notifications.assert_called_once_with("jahan")
    finally:
        app.dependency_overrides.clear()


def test_get_user_notifications_user_not_found():
    """test unknown user returns not found"""

    mock_user_repo = Mock()
    mock_user_repo.get_user_by_username.return_value = None

    mock_notification_service = Mock()

    app.dependency_overrides[get_user_repository] = lambda: mock_user_repo
    app.dependency_overrides[get_notification_service] = lambda: mock_notification_service

    try:
        response = client.get("/Notifications/?username=missing_user")

        assert response.status_code == HTTPStatusCode.NOT_FOUND
        assert response.json()["detail"] == ErrorMessages.USER_NOT_FOUND
    finally:
        app.dependency_overrides.clear()


def test_get_role_notifications_admin_allowed(monkeypatch):
    """test admin can retrieve role notifications"""

    mock_auth = Mock()
    mock_auth.check_role.return_value = True

    mock_notification_service = Mock()
    mock_notification_service.get_role_notifications.return_value = [
        {
            "id": "n2",
            "user_id": "manager_1",
            "role": UserRole.MANAGER.value,
            "event_type": NotificationEventType.NEW_PAID_ORDER.value,
            "event_key": f"{NotificationEventType.NEW_PAID_ORDER.value}:101:manager_1",
            "message": "A new paid order 101 is ready for preparation.",
            "order_id": "101",
            "created_at": "2026-03-21T12:05:00+00:00"
        }
    ]

    app.dependency_overrides[get_auth_service] = lambda: mock_auth
    app.dependency_overrides[get_notification_service] = lambda: mock_notification_service

    try:
        response = client.get(f"/Notifications/role?role={UserRole.MANAGER.value}&username=admin_user")

        assert response.status_code == HTTPStatusCode.OK
        assert response.json()["role"] == UserRole.MANAGER.value
        assert len(response.json()["notifications"]) == 1
        assert response.json()["notifications"][0]["role"] == UserRole.MANAGER.value

        mock_auth.check_role.assert_called_once_with("admin_user", UserRole.ADMIN.value)
        mock_notification_service.get_role_notifications.assert_called_once_with(UserRole.MANAGER.value)
    finally:
        app.dependency_overrides.clear()


def test_get_role_notifications_admin_denied(monkeypatch):
    """test non-admin user cannot retrieve role notifications"""

    def mock_check_role(self, username, required_role):
        raise PermissionError(ErrorMessages.INSUFFICIENT_PERMISSIONS)

    monkeypatch.setattr(AuthService, "check_role", mock_check_role)

    response = client.get(f"/Notifications/role?role={UserRole.MANAGER.value}&username=regular_user")

    assert response.status_code == HTTPStatusCode.FORBIDDEN
    assert response.json()["detail"] == ErrorMessages.INSUFFICIENT_PERMISSIONS


def test_get_user_notifications_with_mocked_services():
    """test notification endpoint with dependency injection mocking"""

    mock_user_repo = Mock()
    mock_user_repo.get_user_by_username.return_value = {
        "username": "test_user",
        "role": "user"
    }

    mock_notification_service = Mock()
    mock_notification_service.get_user_notifications.return_value = [
        {"id": "1", "message": "Test notification", "user_id": "test_user"}
    ]

    app.dependency_overrides[get_user_repository] = lambda: mock_user_repo
    app.dependency_overrides[get_notification_service] = lambda: mock_notification_service

    try:
        response = client.get("/Notifications/?username=test_user")

        assert response.status_code == HTTPStatusCode.OK
        assert response.json()["username"] == "test_user"
        assert len(response.json()["notifications"]) == 1

        mock_user_repo.get_user_by_username.assert_called_once_with("test_user")
        mock_notification_service.get_user_notifications.assert_called_once_with("test_user")
    finally:
        app.dependency_overrides.clear()


def test_get_role_notifications_with_mocked_auth():
    """test role notifications endpoint with mocked auth service"""

    mock_auth = Mock()
    mock_auth.check_role.return_value = True

    mock_notification_service = Mock()
    mock_notification_service.get_role_notifications.return_value = [
        {"id": "1", "role": UserRole.MANAGER.value, "message": "Manager notification"}
    ]

    app.dependency_overrides[get_auth_service] = lambda: mock_auth
    app.dependency_overrides[get_notification_service] = lambda: mock_notification_service

    try:
        response = client.get(f"/Notifications/role?role={UserRole.MANAGER.value}&username=admin")

        assert response.status_code == HTTPStatusCode.OK
        assert response.json()["role"] == UserRole.MANAGER.value

        mock_auth.check_role.assert_called_once_with("admin", UserRole.ADMIN.value)
        mock_notification_service.get_role_notifications.assert_called_once_with(UserRole.MANAGER.value)
    finally:
        app.dependency_overrides.clear()
