from enum import Enum
from pydantic import BaseModel, Field
from typing import List


class OrderStatus(str, Enum):
    pending = "pending"
    preparing = "preparing"
    in_transit = "in-transit"
    delivered = "delivered"
    cancelled = "cancelled"


class OrderItemRequest(BaseModel):
    id: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1)


class CreateOrderRequest(BaseModel):
    username: str = Field(..., min_length=1)
    is_premium: bool = False
    items: List[OrderItemRequest]


class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatus