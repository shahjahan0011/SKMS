from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException

from app.storage.repositories.order_repository import (
    get_order_by_id,
    update_order,
    save_order,
    get_menu_item_by_id,
    get_active_orders_by_restaurant,
    get_orders_by_username,
)
from app.storage.repositories.order_items_repository import save_order_item
from app.schemas.order_schema import OrderStatus
from app.services.notification_service import NotificationService
from app.services.cost_service import calculate_total_breakdown


def _now_iso() -> str:
    return datetime.utcnow().isoformat()

def _validate_status_transition(current: str, new: str) -> None:
    valid_transitions = {
        "pending": {"paid", "cancelled"},
        "paid": {"preparing"},
        "preparing": {"in-transit"},
        "in-transit": {"delivered"},
        "delivered": set(),
        "cancelled": set(),
    }
    
    if new not in valid_transitions.get(current, set()):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from '{current}' to '{new}'",
        )

def create_order(username: str, items: list[dict], is_premium: bool = False) -> dict:
    
    validated_items = []
    restaurant_id = None
    
    for item in items:
        menu_item = get_menu_item_by_id(item["id"])
        if not menu_item:
            raise HTTPException(status_code=404, detail=f"Menu item not found: {item['id']}")
        
        if restaurant_id is None:
            restaurant_id = menu_item.get("restaurant_id")
        elif restaurant_id != menu_item.get("restaurant_id"):
            raise HTTPException(status_code=400, detail="All items must be from same restaurant")
        
        validated_items.append(item)
    
    cost_breakdown = calculate_total_breakdown(validated_items, is_premium=is_premium)
    
    now = _now_iso()
    
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
    }
    
    saved_order = save_order(order)
    
    # Save all items
    for item in validated_items:
        try:
            menu_item = get_menu_item_by_id(item["id"])
            price = float(menu_item.get("price", 0)) if menu_item else 0.0
            save_order_item(
                order_id=saved_order["order_id"],
                item_id=item["id"],
                quantity=item["quantity"],
                item_price=price,
            )
        except Exception as e:
            print(f"Warning: Failed to save order item: {e}")
    
    try:
        NotificationService().notify_order_created(username, saved_order["order_id"])
    except Exception:
        pass
    
    return saved_order

def update_order_status(order_id: str, new_status: str) -> dict:
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    current_status = order.get("status", "")
    
    if not current_status:
        raise HTTPException(status_code=400, detail="Order has invalid status")

    _validate_status_transition(current_status, new_status)

    order["status"] = new_status
    order["updated_at"] = _now_iso()

    if new_status == "delivered":
        order["delivered_at"] = _now_iso()

    updated_order = update_order(order)
    if not updated_order:
        raise HTTPException(status_code=500, detail="Failed to update order")
    
    try:
        NotificationService().notify_order_status_changed(
                updated_order["username"],
                updated_order["order_id"],
                new_status
            )
    except Exception:
        pass

    return updated_order

def cancel_order(order_id: str) -> dict:
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.get("status") != OrderStatus.pending.value:
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be cancelled",
        )

    order["status"] = OrderStatus.cancelled.value
    order["updated_at"] = _now_iso()
    order["cancelled_at"] = _now_iso()

    updated_order = update_order(order)
    if not updated_order:
        raise HTTPException(status_code=500, detail="Failed to cancel order")

    return updated_order

def list_active_orders(restaurant_id: str) -> list[dict]:
    return get_active_orders_by_restaurant(restaurant_id)

def get_order_history(username: str) -> list[dict]:
    from app.storage.repositories.order_items_repository import get_order_items
    
    user_orders = get_orders_by_username(username)
    
    for order in user_orders:
        order["items"] = get_order_items(order.get("order_id", ""))
    
    user_orders.sort(key=lambda o: o.get("created_at", ""), reverse=True)
    
    return user_orders