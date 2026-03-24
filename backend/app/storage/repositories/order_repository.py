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
        return [order for order in reader]  

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
    
    # Filter to FIELDNAMES only - prevents extra columns from being written to CSV
    filtered_order = {k: v for k, v in order_data.items() if k in FIELDNAMES}
    
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(filtered_order)

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
    """
    Update an existing order in the CSV.
    
    Reads all orders, finds the one to update, replaces it, and writes back.
    """
    orders = get_all_orders()
    updated = None
    order_found = False

    # Find and update the order
    for index, order in enumerate(orders):
        if order.get("order_id") == updated_order.get("order_id"):
            # Merge: keep all existing fields, update with new values
            merged_order = {**order, **updated_order}
            # Filter to FIELDNAMES only
            filtered_order = {k: v for k, v in merged_order.items() if k in FIELDNAMES}
            orders[index] = filtered_order
            updated = filtered_order
            order_found = True
            break

    if not order_found:
        return None

    # Write back to CSV
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, extrasaction="ignore")
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