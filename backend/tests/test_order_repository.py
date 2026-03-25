import pytest
from app.storage.repositories.order_repository import (
    save_order,
    get_order_by_id,
    update_order,
    get_active_orders_by_restaurant,
)


def test_save_and_get_order_by_id():
    order = {
        "order_id": "o1",
        "username": "user1",
        "restaurant_id": "rest_1",
        "is_premium": "false",
        "base_cost": "20.00",
        "tax": "1.00",
        "delivery_fee": "4.99",
        "total": "25.99",
        "status": "pending",
        "created_at": "2026-03-24T10:00:00",
        "updated_at": "2026-03-24T10:00:00",
        "cancelled_at": "",
        "delivered_at": "",
    }

    saved = save_order(order)
    retrieved = get_order_by_id("o1")

    assert retrieved is not None
    assert retrieved["username"] == "user1"
    assert retrieved["status"] == "pending"
    assert retrieved["total"] == "25.99"


def test_save_order_filters_extra_fields():
    order = {
        "order_id": "o2",
        "username": "user2",
        "restaurant_id": "rest_2",
        "is_premium": "true",
        "base_cost": "30.00",
        "tax": "1.50",
        "delivery_fee": "0.00",
        "total": "31.50",
        "status": "pending",
        "created_at": "2026-03-24T10:00:00",
        "updated_at": "2026-03-24T10:00:00",
        "cancelled_at": "",
        "delivered_at": "",
        "id": "item_1",  # Extra field
        "quantity": "2",  # Extra field
        "price": "15.00",  # Extra field
    }

    saved = save_order(order)

    # Verify extra fields are NOT in saved order
    assert "id" not in saved
    assert "quantity" not in saved
    assert "price" not in saved
    # But required fields ARE there
    assert saved["username"] == "user2"
    assert saved["is_premium"] == "true"


def test_update_order():
    original_order = {
        "order_id": "o3",
        "username": "user3",
        "restaurant_id": "rest_3",
        "is_premium": "false",
        "base_cost": "20.00",
        "tax": "1.00",
        "delivery_fee": "4.99",
        "total": "25.99",
        "status": "pending",
        "created_at": "2026-03-24T10:00:00",
        "updated_at": "2026-03-24T10:00:00",
        "cancelled_at": "",
        "delivered_at": "",
    }

    save_order(original_order)

    updated_order = {
        **original_order,
        "status": "preparing",
        "updated_at": "2026-03-24T10:05:00",
    }

    result = update_order(updated_order)

    assert result is not None
    assert result["status"] == "preparing"
    assert result["updated_at"] == "2026-03-24T10:05:00"

    retrieved = get_order_by_id("o3")
    assert retrieved is not None
    assert retrieved["status"] == "preparing"


def test_get_active_orders_by_restaurant():
    orders = [
        {
            "order_id": "o4",
            "username": "user4",
            "restaurant_id": "rest_4",
            "is_premium": "false",
            "base_cost": "20.00",
            "tax": "1.00",
            "delivery_fee": "4.99",
            "total": "25.99",
            "status": "pending",
            "created_at": "2026-03-24T10:00:00",
            "updated_at": "2026-03-24T10:00:00",
            "cancelled_at": "",
            "delivered_at": "",
        },
        {
            "order_id": "o5",
            "username": "user5",
            "restaurant_id": "rest_4",
            "is_premium": "false",
            "base_cost": "30.00",
            "tax": "1.50",
            "delivery_fee": "0.00",
            "total": "31.50",
            "status": "preparing",
            "created_at": "2026-03-24T10:05:00",
            "updated_at": "2026-03-24T10:05:00",
            "cancelled_at": "",
            "delivered_at": "",
        },
        {
            "order_id": "o6",
            "username": "user6",
            "restaurant_id": "rest_4",
            "is_premium": "false",
            "base_cost": "15.00",
            "tax": "0.75",
            "delivery_fee": "4.99",
            "total": "20.74",
            "status": "delivered",
            "created_at": "2026-03-24T09:00:00",
            "updated_at": "2026-03-24T10:00:00",
            "cancelled_at": "",
            "delivered_at": "2026-03-24T10:00:00",
        },
    ]

    for order in orders:
        save_order(order)

    active = get_active_orders_by_restaurant("rest_4")

    assert len(active) == 2
    assert all(o.get("status") in {"pending", "preparing"} for o in active)