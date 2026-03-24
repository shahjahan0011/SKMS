import csv
from pathlib import Path
from typing import List, Optional
from uuid import uuid4


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "order_items.csv"

FIELDNAMES = [
    "order_item_id",
    "order_id",
    "item_id",
    "quantity",
    "item_price",
]


def _ensure_file_exists() -> None:
    """Ensure order_items.csv exists with headers."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def save_order_item(order_id: str, item_id: str, quantity: int, item_price: float) -> dict:
    """
    Save a single item in an order.
    
    Args:
        order_id: The order this item belongs to
        item_id: The menu item ID
        quantity: How many of this item
        item_price: Price per unit at order time
        
    Returns:
        Order item dictionary with generated order_item_id
    """
    _ensure_file_exists()
    
    order_item = {
        "order_item_id": str(uuid4()),
        "order_id": order_id,
        "item_id": item_id,
        "quantity": str(quantity),
        "item_price": f"{float(item_price):.2f}",
    }
    
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(order_item)
    
    return order_item


def get_order_items(order_id: str) -> List[dict]:
    """
    Get all items in an order.
    
    Args:
        order_id: The order ID to fetch items for
        
    Returns:
        List of order items dictionaries
    """
    _ensure_file_exists()
    
    items = []
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("order_id") == order_id:
                items.append(row)
    
    return items


def get_all_order_items() -> List[dict]:
    """
    Get all items from all orders.
    
    Returns:
        List of all order items
    """
    _ensure_file_exists()
    
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def delete_order_items(order_id: str) -> None:
    """
    Delete all items for an order (when order is cancelled).
    
    Args:
        order_id: The order whose items to delete
    """
    _ensure_file_exists()
    
    all_items = get_all_order_items()
    remaining_items = [item for item in all_items if item["order_id"] != order_id]
    
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(remaining_items)