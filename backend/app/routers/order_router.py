from fastapi import APIRouter

from app.schemas.order_schema import UpdateOrderStatusRequest
from app.services.order_service import get_order_status, update_order_status, create_order, cancel_order, list_active_orders
from app.schemas.order_schema import CreateOrderRequest
router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/")
def create_new_order(payload: CreateOrderRequest):
    items = [{"id": item.id, "quantity": item.quantity} for item in payload.items]

    return create_order(
        username=payload.username,
        items=items,
        is_premium=payload.is_premium,
    )


@router.get("/{order_id}")
def get_order(order_id: str):
    return get_order_status(order_id)


@router.patch("/{order_id}/status")
def patch_order_status(order_id: str, payload: UpdateOrderStatusRequest):
    return update_order_status(order_id, payload.status.value)


@router.patch("/{order_id}/cancel")
def patch_cancel_order(order_id: str):
    return cancel_order(order_id)


@router.get("/restaurant/{restaurant_id}/active")
def get_active_orders_for_restaurant(restaurant_id: str):
    return list_active_orders(restaurant_id)