from datetime import datetime
from uuid import uuid4

from repositories.order_repository import save_order
from repositories.order_repository import get_menu_item_by_id
from app.schemas.order_schema import OrderStatus


TAX_RATE = 0.05
DELIVERY_FEE = 4.99


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def _safe_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def create_order(username: str, id: str, quantity: int) -> dict:
    menu_item = get_menu_item_by_id(id)
    if menu_item is None:
        raise ValueError(f"Menu item not found: {id}")

    restaurant_id = menu_item.get("restaurant_id")
    price = _safe_float(menu_item.get("price"))

    subtotal = round(price * quantity, 2)
    tax = round(subtotal * TAX_RATE, 2)
    total = round(subtotal + tax + DELIVERY_FEE, 2)
    now = _now_iso()

    order = {
        "order_id": str(uuid4()),
        "username": username,
        "restaurant_id": restaurant_id,
        "id": id,
        "quantity": str(quantity),
        "price": f"{price:.2f}",
        "subtotal": f"{subtotal:.2f}",
        "tax": f"{tax:.2f}",
        "delivery_fee": f"{DELIVERY_FEE:.2f}",
        "total": f"{total:.2f}",
        "status": OrderStatus.pending.value,
        "created_at": now,
        "updated_at": now,
        "cancelled_at": "",
        "delivered_at": "",
    }

    return save_order(order)