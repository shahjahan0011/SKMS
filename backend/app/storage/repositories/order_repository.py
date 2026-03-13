import csv
from pathlib import Path
from typing import List, Optional


DATA_FILE = Path(__file__).resolve().parents[1] / "storage" / "data" / "orders.csv"

FIELDNAMES = [
    "order_id",
    "username",
    "restaurant_id",
    "id",
    "quantity",
    "price",
    "subtotal",
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
        return list(reader)


def get_order_by_id(order_id: str) -> Optional[dict]:
    for order in get_all_orders():
        if order["order_id"] == order_id:
            return order
    return None


def save_order(order_data: dict) -> dict:
    _ensure_file_exists()
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(order_data)
    return order_data