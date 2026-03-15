"""Test menu pagination functionality."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_menu_pagination():
    """Test menu pagination."""
    response = client.get("/menus/1?page=1&page_size=2")
    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert "total_items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 1

def test_menu_search_filtering():
    """Test menu search filtering."""
    response = client.get("/menus/1?search=burger")
    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert isinstance(data["items"], list)

    for item in data["items"]:
        assert "burger" in item["item_name"].lower() or "burger" in item.get("description", "").lower()


def test_page_numbering():
    """Test page numbering."""
    response = client.get("/menus/1?page=2&page_size=2")
    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert isinstance(data["items"], list)


def test_page_size_limits():
    """Test page size limits."""
    response = client.get("/menus/1?page=1&page_size=150")
    assert response.status_code == 422

    response = client.get("/menus/1?page=1&page_size=0")
    assert response.status_code == 422
