from enum import Enum
from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    pending = "pending"
    preparing = "preparing"
    in_transit = "in-transit"
    delivered = "delivered"
    cancelled = "cancelled"


class CreateOrderRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    menu_item_id: str = Field(..., min_length=1)
    quantity: int = Field(default=1, ge=1)