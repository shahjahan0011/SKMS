import pytest

from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.storage.repositories.menu_repository import menu_repository
from app.storage.repositories.restaurant_repository import restaurant_repository

@pytest.fixture
def client():
    """Provides a TestClient for router/integration tests."""
    return TestClient(app)

@pytest.fixture
def mock_menu_repo():
    """Provides a menu repository instance for testing."""
    return menu_repository()

@pytest.fixture
def mock_restaurant_repo():
    """Provides a restaurant repository instance for testing."""
    return restaurant_repository()

@pytest.fixture(autouse=True)
def clear_order_items_csv():
    """Clears the order_items CSV before each test to prevent data leaks."""
    order_items_path = Path(__file__).resolve().parents[1] / "app" / "storage" /"data" / "order_items.csv"
    if order_items_path.exists():
        with open(order_items_path, "w", newline="", encoding="utf-8") as f:
            f.write("order_item_id,order_id,item_id,quantity,item_price\n")
    yield
