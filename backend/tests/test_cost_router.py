import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import cost_router


client = TestClient(app)


def test_preview_base_cost_route(monkeypatch):
    """Test cost preview base cost endpoint"""
    
    def mock_calculate_base_cost(items):
        return 20.00

    monkeypatch.setattr(cost_router, "calculate_base_cost", mock_calculate_base_cost)

    response = client.post(
        "/cost/preview/base",
        json={
            "username": "jahan",
            "is_premium": False,
            "items": [
                {"id": "item_1", "quantity": 2},
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["base_cost"] == 20.00


def test_preview_tax_cost_route(monkeypatch):
    """Test cost preview with tax endpoint"""
    
    def mock_calculate_base_cost(items):
        return 20.00

    def mock_calculate_tax(base_cost):
        return 1.00

    monkeypatch.setattr(cost_router, "calculate_base_cost", mock_calculate_base_cost)
    monkeypatch.setattr(cost_router, "calculate_tax", mock_calculate_tax)

    response = client.post(
        "/cost/preview/tax",
        json={
            "username": "jahan",
            "is_premium": False,
            "items": [
                {"id": "item_1", "quantity": 2},
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["base_cost"] == 20.00
    assert data["tax"] == 1.00
    assert data["base_cost_with_tax"] == 21.00


def test_preview_full_cost_route_standard_user(monkeypatch):
    """Test full cost preview endpoint for standard user"""
    
    def mock_calculate_total_breakdown(items, is_premium=False):
        return {
            "base_cost": 20.00,
            "tax": 1.00,
            "delivery_fee": 4.99,
            "total": 25.99,
        }

    monkeypatch.setattr(cost_router, "calculate_total_breakdown", mock_calculate_total_breakdown)

    response = client.post(
        "/cost/preview/full",
        json={
            "username": "jahan",
            "is_premium": False,
            "items": [
                {"id": "item_1", "quantity": 2},
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["base_cost"] == 20.00
    assert data["tax"] == 1.00
    assert data["delivery_fee"] == 4.99
    assert data["total"] == 25.99


def test_preview_full_cost_route_premium_user(monkeypatch):
    """Test full cost preview endpoint for premium user"""
    
    def mock_calculate_total_breakdown(items, is_premium=False):
        return {
            "base_cost": 20.00,
            "tax": 1.00,
            "delivery_fee": 0.0,
            "total": 21.00,
        }

    monkeypatch.setattr(cost_router, "calculate_total_breakdown", mock_calculate_total_breakdown)

    response = client.post(
        "/cost/preview/full",
        json={
            "username": "jahan",
            "is_premium": True,
            "items": [
                {"id": "item_1", "quantity": 2},
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["base_cost"] == 20.00
    assert data["tax"] == 1.00
    assert data["delivery_fee"] == 0.0
    assert data["total"] == 21.00


def test_preview_full_cost_route_multiple_items(monkeypatch):
    """Test full cost preview with multiple items"""
    
    def mock_calculate_total_breakdown(items, is_premium=False):
        assert len(items) == 2
        return {
            "base_cost": 35.00,
            "tax": 1.75,
            "delivery_fee": 4.99,
            "total": 41.74,
        }

    monkeypatch.setattr(cost_router, "calculate_total_breakdown", mock_calculate_total_breakdown)

    response = client.post(
        "/cost/preview/full",
        json={
            "username": "jahan",
            "is_premium": False,
            "items": [
                {"id": "item_1", "quantity": 2},
                {"id": "item_2", "quantity": 1},
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["base_cost"] == 35.00
    assert data["total"] == 41.74