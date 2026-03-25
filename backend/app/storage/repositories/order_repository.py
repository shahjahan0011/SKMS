import csv
from pathlib import Path
from typing import List, Optional


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
MENU_DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "menus.csv"

FIELDNAMES = [
    "order_id",
    "username",
    "restaurant_id",
    "is_premium",
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


def _ensure_file_exists() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

def get_all_orders() -> List[dict]:
    _ensure_file_exists()
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader) if reader else []

def get_order_by_id(order_id: str) -> Optional[dict]:
    order_id = str(order_id).strip()
    orders = get_all_orders()
    
    for order in orders:
        if str(order.get("order_id", "")).strip() == order_id:
            return order
    return None

def save_order(order_data: dict) -> dict:
    _ensure_file_exists()
    filtered_order = {k: v for k, v in order_data.items() if k in FIELDNAMES}
    
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(filtered_order)
    
    return filtered_order

def get_menu_item_by_id(id: str) -> Optional[dict]:
    try:
        with open(MENU_DATA_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if not reader:
                return None
            for row in reader:
                if row.get("id") == id:
                    return row
    except FileNotFoundError:
        return None
    return None

def update_order(updated_order: dict) -> Optional[dict]:
    orders = get_all_orders()
    updated = None

    for index, order in enumerate(orders):
        if order.get("order_id") == updated_order.get("order_id"):
            merged = {**order, **updated_order}
            filtered = {k: v for k, v in merged.items() if k in FIELDNAMES}
            orders[index] = filtered
            updated = filtered
            break

    if updated is None:
        return None

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(orders)

    return updated

def _filter_orders(predicate) -> list[dict]:
    return [o for o in get_all_orders() if predicate(o)]

def get_orders_by_username(username: str) -> List[dict]:
    return _filter_orders(lambda o: o.get("username") == username)

def get_active_orders_by_restaurant(restaurant_id: str) -> list[dict]:
    active_statuses = {"pending","paid", "preparing", "in-transit"}
    
    filtered = _filter_orders(
        lambda o: o.get("restaurant_id") == restaurant_id 
        and o.get("status") in active_statuses
    )
    filtered.sort(key=lambda o: o.get("created_at", ""))
    return filtered
