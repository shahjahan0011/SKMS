import csv
from pathlib import Path
from typing import List, Optional


DATA_FILE = Path(__file__).resolve().parents[1] / "storage" / "data" / "orders.csv"
MENU_DATA_FILE = Path(__file__).resolve().parents[1] / "storage" / "data" / "menus.csv"
ORDER_ITEMS_FILE = Path(__file__).resolve().parents[1] / "storage" / "data" / "order_items.csv"

FIELDNAMES = [
    "order_id",
    "username",
    "restaurant_id",
    "base_cost",
    "tax",
    "delivery_fee",
    "total",
    "status",
    "created_at",
    "updated_at",
    "cancelled_at",
    "delivered_at",
]

ORDER_ITEM_FIELDNAMES = [
    "order_id",
    "item_id",
    "quantity",
    "unit_price",
    "line_total",
]


def _ensure_file_exists() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def _ensure_order_items_file_exists() -> None:
    ORDER_ITEMS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not ORDER_ITEMS_FILE.exists():
        with open(ORDER_ITEMS_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=ORDER_ITEM_FIELDNAMES)
            writer.writeheader()


def get_all_orders() -> List[dict]:
    _ensure_file_exists()
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def get_order_by_id(order_id: str) -> Optional[dict]:
    order_id = str(order_id).strip()

    orders = get_all_orders()
    order_map = {
        str(order.get("order_id", "")).strip(): order
        for order in orders
    }

    return order_map.get(order_id)


def save_order(order_data: dict) -> dict:
    _ensure_file_exists()
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(order_data)
    return order_data


def get_menu_item_by_id(id: str) -> Optional[dict]:
    with open(MENU_DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row_id = row.get("id")
            if row_id == id:
                return row
    return None


def update_order(updated_order: dict) -> Optional[dict]:
    orders = get_all_orders()
    updated = None

    for index, order in enumerate(orders):
        if order["order_id"] == updated_order["order_id"]:
            orders[index] = updated_order
            updated = updated_order
            break

    if updated is None:
        return None

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(orders)

    return updated


def get_active_orders_by_restaurant(restaurant_id: str) -> list[dict]:
    active_statuses = {"pending", "preparing", "in-transit"}

    orders = [
        order for order in get_all_orders()
        if order["restaurant_id"] == restaurant_id and order["status"] in active_statuses
    ]

    orders.sort(key=lambda order: order["created_at"])
    return orders


def save_order_item(order_item: dict) -> dict:
    _ensure_order_items_file_exists()
    with open(ORDER_ITEMS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=ORDER_ITEM_FIELDNAMES)
        writer.writerow(order_item)
    return order_item


def get_order_items(order_id: str) -> list[dict]:
    _ensure_order_items_file_exists()
    with open(ORDER_ITEMS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader if row["order_id"] == order_id]


def get_orders_by_username(username: str) -> list[dict]:
    return [order for order in get_all_orders() if order["username"] == username]