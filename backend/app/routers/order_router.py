from fastapi import APIRouter

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