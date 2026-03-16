import pytest
from app.storage.repositories.menu_repository import menu_repository
from app.storage.repositories.restaurant_repository import restaurant_repository


@pytest.fixture
def mock_menu_repo():
    repo = menu_repository()
    return repo


@pytest.fixture
def mock_restaurant_repo():
    repo = restaurant_repository()
    return repo