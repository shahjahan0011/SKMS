"""endpoint testing for notification router"""
import csv
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.storage.repositories.user_repository import user_repository
from app.storage.repositories.notification_repository import notification_repository
from app.services.auth_service import auth_service
from app.constants import HTTPStatusCode, UserRole, NotificationEventType, ErrorMessages 


client = TestClient(app)


def setup_test_user_csv(file_path):
    """create temporary user csv for notification router tests"""

    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password", "role"])
        writer.writerow(["jahan", "password123", UserRole.USER.value])  
        writer.writerow(["admin_user", "password123", UserRole.ADMIN.value])  


def setup_test_notification_csv(file_path):
    """create temporary notification csv for router tests"""

    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "user_id", "role", "event_type", "event_key", "message", "order_id", "created_at"])
        writer.writerow([
            "n1",
            "jahan",
            UserRole.CUSTOMER.value, 
            NotificationEventType.ORDER_CREATED.value,  
            f"{NotificationEventType.ORDER_CREATED.value}:101:jahan", 
            "Your order 101 was created successfully.",
            "101",
            "2026-03-21T12:00:00+00:00"
        ])
        writer.writerow([
            "n2",
            "manager_1",
            UserRole.MANAGER.value,  # ✅ CHANGED from "manager"
            NotificationEventType.NEW_PAID_ORDER.value,  # ✅ CHANGED
            f"{NotificationEventType.NEW_PAID_ORDER.value}:101:manager_1",  # ✅ CHANGED
            "A new paid order 101 is ready for preparation.",
            "101",
            "2026-03-21T12:05:00+00:00"
        ])



def get_test_user_file_path():
    """return temporary user csv path"""

    return Path(__file__).resolve().parent / "test_notification_router_users.csv"


def get_test_notification_file_path():
    """return temporary notification csv path"""

    return Path(__file__).resolve().parent / "test_notification_router_notifications.csv"


def patch_user_repository_file(test_file):
    """patch user repository file path"""

    original_init = user_repository.__init__

    def patched_init(self):
        self.file_path = test_file

    user_repository.__init__ = patched_init
    return original_init


def patch_notification_repository_file(test_file):
    """patch notification repository file path"""

    original_init = notification_repository.__init__

    def patched_init(self):
        self.file_path = test_file

    notification_repository.__init__ = patched_init
    return original_init


def restore_repository_init(original_init, repository_class):
    """restore original repository init"""

    repository_class.__init__ = original_init


def test_get_user_notifications():
    """test user notification retrieval endpoint"""

    user_file = get_test_user_file_path()
    notification_file = get_test_notification_file_path()

    setup_test_user_csv(user_file)
    setup_test_notification_csv(notification_file)

    original_user_init = patch_user_repository_file(user_file)
    original_notification_init = patch_notification_repository_file(notification_file)

    response = client.get("/notifications/?username=jahan")

    assert response.status_code == HTTPStatusCode.OK  
    assert response.json()["username"] == "jahan"
    assert len(response.json()["notifications"]) == 1
    assert response.json()["notifications"][0]["user_id"] == "jahan"

    restore_repository_init(original_user_init, user_repository)
    restore_repository_init(original_notification_init, notification_repository)
    user_file.unlink()
    notification_file.unlink()


def test_get_user_notifications_user_not_found():
    """test unknown user returns not found"""

    user_file = get_test_user_file_path()
    notification_file = get_test_notification_file_path()

    setup_test_user_csv(user_file)
    setup_test_notification_csv(notification_file)

    original_user_init = patch_user_repository_file(user_file)
    original_notification_init = patch_notification_repository_file(notification_file)

    response = client.get("/notifications/?username=missing_user")

    assert response.status_code == HTTPStatusCode.NOT_FOUND  
    assert response.json()["detail"] == ErrorMessages.USER_NOT_FOUND  

    restore_repository_init(original_user_init, user_repository)
    restore_repository_init(original_notification_init, notification_repository)
    user_file.unlink()
    notification_file.unlink()


def test_get_role_notifications_admin_allowed(monkeypatch):
    """test admin can retrieve role notifications"""

    notification_file = get_test_notification_file_path()
    setup_test_notification_csv(notification_file)

    original_notification_init = patch_notification_repository_file(notification_file)

    def mock_check_role(self, username, required_role):
        return True

    monkeypatch.setattr(auth_service, "check_role", mock_check_role)

    response = client.get(f"/notifications/role?role={UserRole.MANAGER.value}&username=admin_user")  

    assert response.status_code == HTTPStatusCode.OK  
    assert response.json()["role"] == UserRole.MANAGER.value  
    assert len(response.json()["notifications"]) == 1
    assert response.json()["notifications"][0]["role"] == UserRole.MANAGER.value  

    restore_repository_init(original_notification_init, notification_repository)
    notification_file.unlink()


def test_get_role_notifications_admin_denied(monkeypatch):
    """test non-admin user cannot retrieve role notifications"""

    def mock_check_role(self, username, required_role):
        raise PermissionError(ErrorMessages.INSUFFICIENT_PERMISSIONS)  

    monkeypatch.setattr(auth_service, "check_role", mock_check_role)

    response = client.get(f"/notifications/role?role={UserRole.MANAGER.value}&username=regular_user")  

    assert response.status_code == HTTPStatusCode.FORBIDDEN 
    assert response.json()["detail"] == ErrorMessages.INSUFFICIENT_PERMISSIONS  
    
def test_get_user_notifications_with_mocked_services():
    """test notification endpoint with dependency injection mocking"""
    
    from unittest.mock import Mock
    from app.dependencies import get_user_repository, get_notification_service
    
    mock_user_repo = Mock()
    mock_user_repo.get_user_by_username.return_value = {
        "username": "test_user",
        "role": "user"
    }
    
    mock_notification_service = Mock()
    mock_notification_service.get_user_notifications.return_value = [
        {"id": "1", "message": "Test notification", "user_id": "test_user"}
    ]
    
    # Override both dependencies
    app.dependency_overrides[get_user_repository] = lambda: mock_user_repo
    app.dependency_overrides[get_notification_service] = lambda: mock_notification_service
    
    try:
        response = client.get("/notifications/?username=test_user")
        
        assert response.status_code == HTTPStatusCode.OK
        assert response.json()["username"] == "test_user"
        assert len(response.json()["notifications"]) == 1
        
        mock_user_repo.get_user_by_username.assert_called_once_with("test_user")
        mock_notification_service.get_user_notifications.assert_called_once_with("test_user")
    
    finally:
        app.dependency_overrides.clear()


def test_get_role_notifications_with_mocked_auth():
    """test role notifications endpoint with mocked auth service"""
    
    from unittest.mock import Mock
    from app.dependencies import get_auth_service, get_notification_service
    
    mock_auth = Mock()
    mock_auth.check_role.return_value = True
    
    mock_notification_service = Mock()
    mock_notification_service.get_role_notifications.return_value = [
        {"id": "1", "role": UserRole.MANAGER.value, "message": "Manager notification"}
    ]
    
    app.dependency_overrides[get_auth_service] = lambda: mock_auth
    app.dependency_overrides[get_notification_service] = lambda: mock_notification_service
    
    try:
        response = client.get(f"/notifications/role?role={UserRole.MANAGER.value}&username=admin")
        
        assert response.status_code == HTTPStatusCode.OK
        assert response.json()["role"] == UserRole.MANAGER.value
        
        mock_auth.check_role.assert_called_once_with("admin", UserRole.ADMIN.value)
        mock_notification_service.get_role_notifications.assert_called_once_with(UserRole.MANAGER.value)
    
    finally:
        app.dependency_overrides.clear()
        