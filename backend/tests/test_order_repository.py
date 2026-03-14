import csv
from pathlib import Path

from app.storage.repositories import order_repository


def test_save_and_get_order_by_id(tmp_path, monkeypatch):
    temp_orders_file = tmp_path / "orders.csv"

    monkeypatch.setattr(order_repository, "DATA_FILE", temp_orders_file)

    order_repository._ensure_file_exists()

    order = {
        "order_id": "o1",
        "username": "jahan",
        "restaurant_id": "rest_1",
        "id": "item_1",
        "quantity": "2",
        "price": "10.00",
        "subtotal": "20.00",
        "tax": "1.00",
        "delivery_fee": "4.99",
        "total": "25.99",
        "status": "pending",
        "created_at": "2026-03-13T12:00:00",
        "updated_at": "2026-03-13T12:00:00",
        "cancelled_at": "",
        "delivered_at": "",
    }

    saved = order_repository.save_order(order)
    fetched = order_repository.get_order_by_id("o1")

    assert saved["order_id"] == "o1"
    assert fetched is not None
    assert fetched["username"] == "jahan"
    assert fetched["id"] == "item_1"


def test_update_order(tmp_path, monkeypatch):
    temp_orders_file = tmp_path / "orders.csv"
    monkeypatch.setattr(order_repository, "DATA_FILE", temp_orders_file)

    order_repository._ensure_file_exists()

    original = {
        "order_id": "o1",
        "username": "jahan",
        "restaurant_id": "rest_1",
        "id": "item_1",
        "quantity": "1",
        "price": "10.00",
        "subtotal": "10.00",
        "tax": "0.50",
        "delivery_fee": "4.99",
        "total": "15.49",
        "status": "pending",
        "created_at": "2026-03-13T12:00:00",
        "updated_at": "2026-03-13T12:00:00",
        "cancelled_at": "",
        "delivered_at": "",
    }

    order_repository.save_order(original)

    updated_order = original.copy()
    updated_order["status"] = "preparing"
    updated_order["updated_at"] = "2026-03-13T12:05:00"

    result = order_repository.update_order(updated_order)

    assert result is not None
    assert result["status"] == "preparing"

    fetched = order_repository.get_order_by_id("o1")
    assert fetched is not None
    assert fetched["status"] == "preparing"


def test_get_menu_item_by_id(tmp_path, monkeypatch):
    temp_menu_file = tmp_path / "menus.csv"
    monkeypatch.setattr(order_repository, "MENU_DATA_FILE", temp_menu_file)

    with open(temp_menu_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "restaurant_id", "price"])
        writer.writeheader()
        writer.writerow({
            "id": "item_1",
            "restaurant_id": "rest_1",
            "price": "10.00",
        })

    result = order_repository.get_menu_item_by_id("item_1")

    assert result is not None
    assert result["id"] == "item_1"
    assert result["restaurant_id"] == "rest_1"


def test_get_active_orders_by_restaurant(tmp_path, monkeypatch):
    temp_orders_file = tmp_path / "orders.csv"
    monkeypatch.setattr(order_repository, "DATA_FILE", temp_orders_file)

    order_repository._ensure_file_exists()

    orders = [
        {
            "order_id": "o1",
            "username": "u1",
            "restaurant_id": "rest_1",
            "id": "item_1",
            "quantity": "1",
            "price": "10.00",
            "subtotal": "10.00",
            "tax": "0.50",
            "delivery_fee": "4.99",
            "total": "15.49",
            "status": "pending",
            "created_at": "2026-03-13T10:00:00",
            "updated_at": "2026-03-13T10:00:00",
            "cancelled_at": "",
            "delivered_at": "",
        },
        {
            "order_id": "o2",
            "username": "u2",
            "restaurant_id": "rest_1",
            "id": "item_2",
            "quantity": "1",
            "price": "12.00",
            "subtotal": "12.00",
            "tax": "0.60",
            "delivery_fee": "4.99",
            "total": "17.59",
            "status": "preparing",
            "created_at": "2026-03-13T11:00:00",
            "updated_at": "2026-03-13T11:00:00",
            "cancelled_at": "",
            "delivered_at": "",
        },
        {
            "order_id": "o3",
            "username": "u3",
            "restaurant_id": "rest_1",
            "id": "item_3",
            "quantity": "1",
            "price": "8.00",
            "subtotal": "8.00",
            "tax": "0.40",
            "delivery_fee": "4.99",
            "total": "13.39",
            "status": "delivered",
            "created_at": "2026-03-13T12:00:00",
            "updated_at": "2026-03-13T12:00:00",
            "cancelled_at": "",
            "delivered_at": "2026-03-13T12:30:00",
        },
    ]

    for order in orders:
        order_repository.save_order(order)

    result = order_repository.get_active_orders_by_restaurant("rest_1")

    assert len(result) == 2
    assert result[0]["order_id"] == "o1"
    assert result[1]["order_id"] == "o2"
    assert all(order["status"] in {"pending", "preparing", "in-transit"} for order in result)