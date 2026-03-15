from fastapi import APIRouter

from app.schemas.order_schema import UpdateOrderStatusRequest
from app.services.order_service import get_order_status, update_order_status
from app.schemas.order_schema import CreateOrderRequest
from app.services.order_service import create_order

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/")
def create_new_order(payload: CreateOrderRequest):
    return create_order(
        username=payload.username,
        id=payload.id,
        quantity=payload.quantity,
    )

@router.get("/{order_id}")
def get_order(order_id: str):
    return get_order_status(order_id)


@router.patch("/{order_id}/status")
def patch_order_status(order_id: str, payload: UpdateOrderStatusRequest):
    return update_order_status(order_id, payload.status.value)