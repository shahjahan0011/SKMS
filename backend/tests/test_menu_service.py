from unittest.mock import MagicMock
from backend.app.services.menu_services import MenuService

def test_get_global_menus_include_restaurant_name():
    """Test that get_global_menus includes restaurant name in the response."""
    mock_menu_repo = MagicMock()
    mock_res_repo = MagicMock()

    mock_menu_repo.get_menu_by_filters.return_value = [{
        "id": "1",
        "restaurant_id": "res123",
        "item_name": "Test Dish",
        "price": 9.99,
        "is_available": "true"
    }]

    mock_res_repo.get_all.return_value = [
        {"id": "res123", "name": "Test Kitchen"}
    ]

    menu_service = MenuService(mock_menu_repo, mock_res_repo)

    result = menu_service.get_global_menus(item_name="Test Dish")
    assert result[0]["restaurant_name"] == "Test Kitchen"


def test_get_global_menus_missing_restaurant():
    """Test that the service doesn't crash if a restaurant ID is missing."""
    mock_menu_repo = MagicMock()
    mock_res_repo = MagicMock()

    mock_menu_repo.get_menu_by_filters.return_value = [{
        "id": "1",
        "restaurant_id": "res_999",
        "item_name": "Mystery Dish",
        "price": 10.0,
        "is_available": "true"
    }]

    mock_res_repo.get_all.return_value = [{"id": "res_001", "name": "Real Kitchen"}]

    menu_service = MenuService(mock_menu_repo, mock_res_repo)
    result = menu_service.get_global_menus(item_name="Mystery Dish")

    assert len(result) == 1
    assert result[0]["restaurant_name"] == "Unknown Kitchen"


def test_get_global_menus_filters_inactive_items():
    """Test that items with is_available='false' are excluded."""
    mock_menu_repo = MagicMock()
    mock_res_repo = MagicMock()

    mock_menu_repo.get_menu_by_filters.return_value = [
        {"id": "1", "restaurant_id": "res1", "name": "Active Dish", "is_available": "true"},
        {"id": "2", "restaurant_id": "res1", "name": "Inactive Dish", "is_available": "false"}
    ]
    mock_res_repo.get_all.return_value = [{"id": "res1", "name": "Test Kitchen"}]

    menu_service = MenuService(mock_menu_repo, mock_res_repo)
    result = menu_service.get_global_menus()

    assert len(result) == 1
    assert result[0]["name"] == "Active Dish"
