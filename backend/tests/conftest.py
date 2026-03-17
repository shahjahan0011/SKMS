import pytest
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