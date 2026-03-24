"""testing file for roles"""
from fastapi.testclient import TestClient

from app.main import app
from app.services.auth_service import AuthService

client = TestClient(app)


def test_admin_access_denied(monkeypatch):
    """test non-admin user is denied access"""

    def mock_check_role(self, username, required_role):
        raise PermissionError("user does not have required role")

    monkeypatch.setattr(AuthService, "check_role", mock_check_role)

    response = client.get("/auth/admin?username=regular_user")

    assert response.status_code == 403
    assert response.json()["detail"] == "user does not have required role"


def test_admin_access_allowed(monkeypatch):
    """test admin user is granted access"""

    def mock_check_role(self, username, required_role):
        return True

    monkeypatch.setattr(AuthService, "check_role", mock_check_role)

    response = client.get("/auth/admin?username=admin_user")

    assert response.status_code == 200
    assert response.json()["message"] == "admin access granted"


def test_admin_access_user_not_found(monkeypatch):
    """test missing user returns not found"""

    def mock_check_role(self, username, required_role):
        raise ValueError("user does not exist")

    monkeypatch.setattr(AuthService, "check_role", mock_check_role)

    response = client.get("/auth/admin?username=missing_user")

    assert response.status_code == 404
    assert response.json()["detail"] == "user does not exist"
    