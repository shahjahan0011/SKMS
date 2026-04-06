import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.routers.menu_router import get_menu_service

client = TestClient(app)

def override_get_menu_service():
    mock_service = MagicMock()

    mock_service.get_active_menu_paginated_by_restaurant.return_value = {
        "items": [
            {"id": "item_1", "item_name": "Chicken Briyani", "price": 12.99}
        ],
        "total": 1,
        "page": 1,
        "size": 10
    }

    mock_service.get_global_menus.return_value = [
         {"id": "item_1", "item_name": "Chicken Briyani", "price": 12.99}
    ]

    return mock_service

app.dependency_overrides[get_menu_service] = override_get_menu_service


def test_get_menus_status_and_structure():
    """Test global menu browsing returns 200 and a list."""
    response = client.get("/menus")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_menu_by_restaurant_success():
    """Test paginated restaurant menu returns 200 and a dictionary."""
    response = client.get("/menus/13")
    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert data["items"][0]["item_name"] == "Briyani rice"


@pytest.mark.parametrize("invalid_price", [
    "abc",
    "free",
])
def test_global_menus_invalid_price_type(invalid_price):
    """Test that FastAPI correctly blocks non-numeric price queries."""
    response = client.get(f"/menus?price={invalid_price}")

    assert response.status_code == 422


@pytest.mark.parametrize("test_size, expected_status", [
    (0, 422),
    (1, 200),
    (100, 200),
    (101, 422)
])
def test_menu_pagination_boundaries(test_size, expected_status):
    """Test the ge=1 and le=100 FastAPI validation boundaries."""
    response = client.get(f"/menus/13?page_size={test_size}")
    assert response.status_code == expected_status


def test_restaurant_999999_hardcoded_404():
    """Test the specific logic block that forces a 404 for ID 999999 with no items."""

    def override_empty_service():
        mock = MagicMock()
        mock.get_active_menu_paginated_by_restaurant.return_value = {"items": []}
        return mock

    app.dependency_overrides[get_menu_service] = override_empty_service

    response = client.get("/menus/999999")

    assert response.status_code == 404
    assert "Restaurant or menu not found" in response.json()["detail"]

    app.dependency_overrides[get_menu_service] = override_get_menu_service


# M4 inventory restock tests
def test_restock_unauthorized_user():
    """Test that a non-admin user is blocked from restocking."""
    payload = {"added_stock": 50}

    response = client.patch(
        "/menus/1/restock?username=random_customer",
        json=payload
    )

    assert response.status_code in [403, 404]
    assert "detail" in response.json()


def test_restock_success_with_admin(monkeypatch):
    """Test that a valid admin can successfully restock an item."""
    def mock_check_role(self, username , role) -> None:
        pass

    monkeypatch.setattr(
        "app.services.auth_service.AuthService.check_role",
        mock_check_role
    )

    payload = {"added_stock": 20}
    response = client.patch(
        "/menus/1/restock?username=real_admin",
        json=payload
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
