import pytest
from unittest.mock import MagicMock
from backend.app.services.restaurant_service import RestaurantService

@pytest.fixture
def mock_repo():
    repo = MagicMock()

    repo.get_all_restaurants.return_value = [
        {"id": "1", "name": "Pasta Place", "is_active": "true"},
        {"id": "2", "name": "Curry House", "status": "1"},
        {"id": "3", "name": "Burger Joint", "is_active": "false"},
        {"id": "4", "name": "Taco Town", "is_active": "yes"},
    ]
    return repo

def test_browse_restaurants_filters_active_only(mock_repo):
    """Verify service only returns restaurants matching 'true', '1', or 'yes'."""
    service = RestaurantService(mock_repo)
    result = service.browse_restaurants()

    assert result["metadata"]["total_items"] == 3
    names = [r["name"] for r in result["data"]]
    assert "Burger Joint" not in names
    assert "Pasta Place" in names

def test_browse_restaurants_keyword_search(mock_repo):
    """Verify keyword filtering happens after the active filter."""
    service = RestaurantService(mock_repo)

    result = service.browse_restaurants(keyword="Pasta")
    assert result["metadata"]["total_items"] == 1
    assert result["data"][0]["name"] == "Pasta Place"

    result_inactive = service.browse_restaurants(keyword="Burger")
    assert result_inactive["metadata"]["total_items"] == 0

def test_browse_restaurants_pagination_logic(mock_repo):
    """Verify pagination math (limit=2)."""
    service = RestaurantService(mock_repo)

    result = service.browse_restaurants(limit=2, page=1)

    assert len(result["data"]) == 2
    assert result["metadata"]["total_pages"] == 2
    assert result["metadata"]["has_next_page"] is True
