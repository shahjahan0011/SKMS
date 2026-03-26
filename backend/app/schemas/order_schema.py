from enum import Enum
from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    preparing = "preparing"
    in_transit = "in-transit"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderItemRequest(BaseModel):
    id: str = Field(..., min_length=1)
    quantity: int = Field(default=1, ge=1)

class CreateOrderRequest(BaseModel):
    username: str = Field(..., min_length=1)
    items: list[OrderItemRequest] = Field(..., min_length=1)
    is_premium: bool = Field(default=False)

class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatus