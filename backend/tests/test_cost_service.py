import pytest
from fastapi import HTTPException

from app.services import cost_service


def test_calculate_base_cost_single_item(monkeypatch):
    """Test base cost calculation with single item"""
    
    def mock_get_menu_item_by_id(item_id):
        return {
            "id": item_id,
            "restaurant_id": "rest_1",
            "price": "10.00",
        }

    monkeypatch.setattr(cost_service, "get_menu_item_by_id", mock_get_menu_item_by_id)

    items = [{"id": "item_1", "quantity": 2}]
    result = cost_service.calculate_base_cost(items)

    assert result == 20.00


def test_calculate_base_cost_multiple_items(monkeypatch):
    """Test base cost calculation with multiple items"""
    
    def mock_get_menu_item_by_id(item_id):
        prices = {
            "item_1": "10.00",
            "item_2": "15.00",
        }
        return {
            "id": item_id,
            "restaurant_id": "rest_1",
            "price": prices.get(item_id, "0.00"),
        }

    monkeypatch.setattr(cost_service, "get_menu_item_by_id", mock_get_menu_item_by_id)

    items = [
        {"id": "item_1", "quantity": 2},
        {"id": "item_2", "quantity": 1},
    ]
    result = cost_service.calculate_base_cost(items)

    assert result == 35.00  # (10 * 2) + (15 * 1)


def test_calculate_base_cost_invalid_item(monkeypatch):
    """Test base cost calculation fails with invalid item"""
    
    def mock_get_menu_item_by_id(item_id):
        return None

    monkeypatch.setattr(cost_service, "get_menu_item_by_id", mock_get_menu_item_by_id)

    items = [{"id": "bad_item", "quantity": 1}]

    with pytest.raises(HTTPException) as exc:
        cost_service.calculate_base_cost(items)

    assert exc.value.status_code == 404
    assert "Menu item not found" in exc.value.detail


def test_calculate_tax(monkeypatch):
    """Test tax calculation"""
    base_cost = 20.00
    result = cost_service.calculate_tax(base_cost)

    assert result == 1.00  # 20 * 0.05


def test_calculate_delivery_fee_standard_user(monkeypatch):
    """Test delivery fee for standard (non-premium) user with low order"""
    base_cost = 10.00
    result = cost_service.calculate_delivery_fee(base_cost, is_premium=False)

    assert result == 4.99


def test_calculate_delivery_fee_standard_user_high_order(monkeypatch):
    """Test delivery fee for standard user with order >= $20 threshold"""
    base_cost = 20.00
    result = cost_service.calculate_delivery_fee(base_cost, is_premium=False)

    assert result == 0.0  # Free delivery for high order


def test_calculate_delivery_fee_premium_user(monkeypatch):
    """Test delivery fee for premium user (always free)"""
    base_cost = 10.00
    result = cost_service.calculate_delivery_fee(base_cost, is_premium=True)

    assert result == 0.0


def test_calculate_total_breakdown_standard_user(monkeypatch):
    """Test full cost breakdown for standard user"""
    
    def mock_get_menu_item_by_id(item_id):
        return {
            "id": item_id,
            "restaurant_id": "rest_1",
            "price": "10.00",
        }

    monkeypatch.setattr(cost_service, "get_menu_item_by_id", mock_get_menu_item_by_id)

    items = [{"id": "item_1", "quantity": 1}]
    result = cost_service.calculate_total_breakdown(items, is_premium=False)

    assert result["base_cost"] == 10.00
    assert result["tax"] == 0.50
    assert result["delivery_fee"] == 4.99
    assert result["total"] == 15.49


def test_calculate_total_breakdown_premium_user_no_delivery(monkeypatch):
    """Test full cost breakdown for premium user (no delivery fee)"""
    
    def mock_get_menu_item_by_id(item_id):
        return {
            "id": item_id,
            "restaurant_id": "rest_1",
            "price": "10.00",
        }

    monkeypatch.setattr(cost_service, "get_menu_item_by_id", mock_get_menu_item_by_id)

    items = [{"id": "item_1", "quantity": 2}]
    result = cost_service.calculate_total_breakdown(items, is_premium=True)

    assert result["base_cost"] == 20.00
    assert result["tax"] == 1.00
    assert result["delivery_fee"] == 0.0
    assert result["total"] == 21.00


def test_calculate_total_breakdown_high_order_free_delivery(monkeypatch):
    """Test full cost breakdown with order >= $20 (free delivery)"""
    
    def mock_get_menu_item_by_id(item_id):
        return {
            "id": item_id,
            "restaurant_id": "rest_1",
            "price": "15.00",
        }

    monkeypatch.setattr(cost_service, "get_menu_item_by_id", mock_get_menu_item_by_id)

    items = [{"id": "item_1", "quantity": 2}]  # 30.00 base cost
    result = cost_service.calculate_total_breakdown(items, is_premium=False)

    assert result["base_cost"] == 30.00
    assert result["tax"] == 1.50
    assert result["delivery_fee"] == 0.0  # Free because >= $20
    assert result["total"] == 31.50


def test_safe_float_valid_values(monkeypatch):
    """Test _safe_float with valid numeric strings"""
    assert cost_service._safe_float("10.00") == 10.00
    assert cost_service._safe_float("0") == 0.0
    assert cost_service._safe_float(25) == 25.0


def test_safe_float_invalid_values(monkeypatch):
    """Test _safe_float with invalid values (should return 0.0)"""
    assert cost_service._safe_float("invalid") == 0.0
    assert cost_service._safe_float(None) == 0.0
    assert cost_service._safe_float("") == 0.0