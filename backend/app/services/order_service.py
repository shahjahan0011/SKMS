from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException

from app.storage.repositories.order_repository import (
    get_order_by_id,
    update_order,
    save_order,
    get_menu_item_by_id,
    get_active_orders_by_restaurant,
    save_order_item,
)
from app.schemas.order_schema import OrderStatus
from app.services.cost_service import calculate_total_breakdown, _safe_float


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def create_order(username: str, items: list[dict], is_premium: bool = False) -> dict:
    if not items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    first_item = get_menu_item_by_id(items[0]["id"])
    if first_item is None:
        raise HTTPException(status_code=404, detail=f"Menu item not found: {items[0]['id']}")

    restaurant_id = first_item.get("restaurant_id")

    for item in items:
        menu_item = get_menu_item_by_id(item["id"])
        if menu_item is None:
            raise HTTPException(status_code=404, detail=f"Menu item not found: {item['id']}")
        if menu_item.get("restaurant_id") != restaurant_id:
            raise HTTPException(
                status_code=400,
                detail="All items in one order must belong to the same restaurant",
            )

    breakdown = calculate_total_breakdown(items, is_premium=is_premium)

    order_id = str(uuid4())
    now = _now_iso()

    order = {
        "order_id": order_id,
        "username": username,
        "restaurant_id": restaurant_id,
        "base_cost": f"{breakdown['base_cost']:.2f}",
        "tax": f"{breakdown['tax']:.2f}",
        "delivery_fee": f"{breakdown['delivery_fee']:.2f}",
        "total": f"{breakdown['total']:.2f}",
        "status": OrderStatus.pending.value,
        "created_at": now,
        "updated_at": now,
        "cancelled_at": "",
        "delivered_at": "",
    }

    save_order(order)

    for item in items:
        menu_item = get_menu_item_by_id(item["id"])
        if menu_item is None:
            raise HTTPException(status_code=404, detail=f"Menu item not found: {item['id']}")
        unit_price = _safe_float(menu_item.get("price"))
        quantity = item["quantity"]
        line_total = round(unit_price * quantity, 2)

        save_order_item({
            "order_id": order_id,
            "item_id": item["id"],
            "quantity": str(quantity),
            "unit_price": f"{unit_price:.2f}",
            "line_total": f"{line_total:.2f}",
        })

    return order


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