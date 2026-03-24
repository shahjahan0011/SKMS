from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException

from app.storage.repositories.order_repository import (
    get_order_by_id,
    update_order,
    save_order,
    get_menu_item_by_id,
    get_active_orders_by_restaurant,
    get_all_orders,
)
from app.storage.repositories.order_items_repository import save_order_item
from app.schemas.order_schema import OrderStatus
from app.services.notification_service import NotificationService
from app.services.cost_service import calculate_total_breakdown

TAX_RATE = 0.05
DELIVERY_FEE = 4.99


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def _safe_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def create_order(username: str, id: str, quantity: int, is_premium: bool = False) -> dict:
    """
    Create an order (compatibility layer for single-item orders).
    """
    
    menu_item = get_menu_item_by_id(id)
    if menu_item is None:
        raise HTTPException(status_code=404, detail=f"Menu item not found: {id}")

    restaurant_id = menu_item.get("restaurant_id")
    price = _safe_float(menu_item.get("price"))

    # Use cost_service for consistent calculations
    items = [{"id": id, "quantity": quantity}]
    cost_breakdown = calculate_total_breakdown(items, is_premium=is_premium)
    
    now = _now_iso()

    # Create order dict for storage
    order = {
        "order_id": str(uuid4()),
        "username": username,
        "restaurant_id": restaurant_id,
        "is_premium": "true" if is_premium else "false",
        "base_cost": f"{cost_breakdown['base_cost']:.2f}",
        "tax": f"{cost_breakdown['tax']:.2f}",
        "delivery_fee": f"{cost_breakdown['delivery_fee']:.2f}",
        "total": f"{cost_breakdown['total']:.2f}",
        "status": OrderStatus.pending.value,
        "created_at": now,
        "updated_at": now,
        "cancelled_at": "",
        "delivered_at": "",
        # Add item fields here for API response
        # (they won't be saved to CSV due to filtering in save_order())
        "id": id,
        "quantity": str(quantity),
        "price": f"{price:.2f}",
    }

    # save_order filters for CSV but returns full order dict
    saved_order = save_order(order)
    
    # Save item to order_items.csv
    try:
        save_order_item(
            order_id=saved_order["order_id"],
            item_id=id,
            quantity=quantity,
            item_price=price,
        )
    except Exception as e:
        print(f"Warning: Failed to save order item: {e}")

    try:
        NotificationService().notify_order_created(username, saved_order["order_id"])
    except Exception:
        pass

    return saved_order

def get_order_status(order_id: str) -> dict:
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def update_order_status(order_id: str, new_status: str) -> dict:
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    current_status = order["status"]

    valid_transitions = {
        "pending": {"preparing", "cancelled"},
        "preparing": {"in-transit"},
        "in-transit": {"delivered"},
        "delivered": set(),
        "cancelled": set(),
    }

    if new_status not in valid_transitions[current_status]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from '{current_status}' to '{new_status}'",
        )

    order["status"] = new_status
    order["updated_at"] = _now_iso()

    if new_status == "delivered":
        order["delivered_at"] = _now_iso()

    updated_order = update_order(order)
    assert updated_order is not None, "Failed to update order"
    
    try:
        NotificationService().notify_order_status_changed(
            updated_order["username"],
            updated_order["order_id"],
            new_status
        )
    except Exception:
        pass

    return updated_order

def list_active_orders(restaurant_id: str) -> list[dict]:
    return get_active_orders_by_restaurant(restaurant_id)

def cancel_order(order_id: str) -> dict:
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order["status"] != OrderStatus.pending.value:
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be cancelled",
        )

    order["status"] = OrderStatus.cancelled.value
    order["updated_at"] = _now_iso()
    order["cancelled_at"] = _now_iso()

    updated_order = update_order(order)
    assert updated_order is not None, "Failed to update order"
    return updated_order


def get_order_history(username: str) -> list[dict]:
    """
    Get complete order history for a user with items breakdown.
    
    Retrieves all orders for a user and enriches each with:
    - Order items (from order_items.csv)
    - Cost breakdown (already in orders.csv)
    
    Args:
        username: The customer username
        
    Returns:
        List of orders (newest first) with items nested
        
    Example response:
        [
            {
                "order_id": "o1",
                "username": "jahan",
                "restaurant_id": "rest_1",
                "is_premium": "true",
                "base_cost": "35.00",
                "tax": "1.75",
                "delivery_fee": "0.00",
                "total": "36.75",
                "status": "delivered",
                "created_at": "2026-03-24T...",
                "items": [
                    {"order_item_id": "oi1", "order_id": "o1", "item_id": "item_1", "quantity": "2", "item_price": "10.00"},
                    {"order_item_id": "oi2", "order_id": "o1", "item_id": "item_3", "quantity": "1", "item_price": "15.00"}
                ]
            }
        ]
    """
    from app.storage.repositories.order_items_repository import get_order_items
    
    # Get all orders and filter by username
    all_orders = get_all_orders()
    user_orders = [order for order in all_orders if order["username"] == username]
    
    # Enrich each order with its items
    for order in user_orders:
        order_items = get_order_items(order["order_id"])
        order["items"] = order_items
    
    # Sort by created_at descending (newest first)
    user_orders.sort(key=lambda o: o["created_at"], reverse=True)
    
    return user_orders