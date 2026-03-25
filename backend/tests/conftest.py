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

@pytest.fixture(autouse=True)
def clear_notifications_csv():
    """Clears the notifications CSV before each test to prevent data leaks."""
    notifications_path = Path(__file__).resolve().parents[1] / "app" / "storage" / "data" / "notifications.csv"
    if notifications_path.exists():
        with open(notifications_path, "w", newline="", encoding="utf-8") as f:
            f.write("id,user_id,role,event_type,event_key,message,order_id,created_at\n")
    yield
 
 
@pytest.fixture(autouse=True)
def clear_orders_csv():
    """Clears the orders CSV before each test to prevent data leaks."""
    orders_path = Path(__file__).resolve().parents[1] / "app" / "storage" / "data" / "orders.csv"
    if orders_path.exists():
        with open(orders_path, "w", newline="", encoding="utf-8") as f:
            f.write("order_id,username,restaurant_id,is_premium,base_cost,tax,delivery_fee,total,status,created_at,updated_at,cancelled_at,delivered_at\n")
    yield
    