"""endpoint testing along with making its own csv for testing purposes only"""
import csv
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.storage.repositories.user_repository import UserRepository
from app.constants import HTTPStatusCode, UserRole  
from unittest.mock import Mock


client = TestClient(app)


def setup_test_csv(file_path):
    """create temporary csv file for router tests"""

    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password", "role"])


def get_test_file_path():
    """return temporary csv path for router tests"""

    return Path(__file__).resolve().parent / "test_auth_router_users.csv"


def patch_repository_file(test_file):
    """patch repository file path so tests do not use real storage"""

    original_init = UserRepository.__init__

    def patched_init(self):
        self.file_path = test_file

    UserRepository.__init__ = patched_init
    return original_init


def restore_repository_init(original_init):
    """restore original repository init"""

    UserRepository.__init__ = original_init


def test_register_endpoint():
    """test register endpoint returns created user"""

    test_file = get_test_file_path()
    setup_test_csv(test_file)

    original_init = patch_repository_file(test_file)

    response = client.post(
        "/auth/register",
        json={
            "username": "new_router_user",
            "password": "password123",
            "role": UserRole.USER.value
        }
    )

    assert response.status_code == HTTPStatusCode.OK 
    assert response.json()["username"] == "new_router_user"
    assert response.json()["role"] == UserRole.USER.value

    restore_repository_init(original_init)
    test_file.unlink()


def test_login_endpoint():
    """test login endpoint returns logged in user"""

    test_file = get_test_file_path()
    setup_test_csv(test_file)

    original_init = patch_repository_file(test_file)

    client.post(
        "/auth/register",
        json={
            "username": "login_user",
            "password": "password123",
            "role": UserRole.USER.value
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "login_user",
            "password": "password123"
        }
    )

    assert response.status_code == HTTPStatusCode.OK 
    assert response.json()["username"] == "login_user"
    assert response.json()["role"] == UserRole.USER.value

    restore_repository_init(original_init)
    test_file.unlink()


def test_login_endpoint_invalid_credentials():
    """test login endpoint returns error for invalid credentials"""

    test_file = get_test_file_path()
    setup_test_csv(test_file)

    original_init = patch_repository_file(test_file)

    response = client.post(
        "/auth/login",
        json={
            "username": "not_a_user",
            "password": "wrong_password"
        }
    )

    assert response.status_code == HTTPStatusCode.UNAUTHORIZED
    assert "detail" in response.json()

    restore_repository_init(original_init)
    test_file.unlink()


def test_logout_endpoint():
    """test logout endpoint returns success message"""

    response = client.post("/auth/logout")

    assert response.status_code == HTTPStatusCode.OK  
    assert response.json()["message"] == "logout successful"

def test_register_with_mocked_service():
    """test register endpoint with dependency injection mocking"""
    
    from unittest.mock import Mock
    from app.dependencies import get_auth_service
    
    mock_service = Mock()
    mock_service.register_user.return_value = {
        "username": "mocked_user",
        "role": UserRole.USER.value
    }
    
    app.dependency_overrides[get_auth_service] = lambda: mock_service
    
    try:
        response = client.post(
            "/auth/register",
            json={
                "username": "test",
                "password": "pass123",
                "role": "user"
            }
        )
        
        assert response.status_code == HTTPStatusCode.OK
        assert response.json()["username"] == "mocked_user"
        mock_service.register_user.assert_called_once()
    
    finally:
        app.dependency_overrides.clear()


def test_login_with_mocked_service():
    """test login endpoint with dependency injection mocking"""
    
    from unittest.mock import Mock
    from app.dependencies import get_auth_service
    
    mock_service = Mock()
    mock_service.login_user.return_value = {
        "username": "mocked_user",
        "role": UserRole.ADMIN.value
    }
    
    app.dependency_overrides[get_auth_service] = lambda: mock_service
    
    try:
        response = client.post(
            "/auth/login",
            json={
                "username": "test",
                "password": "pass123"
            }
        )
        
        assert response.status_code == HTTPStatusCode.OK
        assert response.json()["username"] == "mocked_user"
        assert response.json()["role"] == UserRole.ADMIN.value
        mock_service.login_user.assert_called_once_with("test", "pass123")
    
    finally:
        app.dependency_overrides.clear()
