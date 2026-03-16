"""Delivery Schema"""

from pydantic import BaseModel
from app.schemas.location_schema import location

class delivery(BaseModel):
    """
    Delivery Information Entity
    """

    order_id: int
    restaurant_id: int
    user_id: int
    user_name: str
    delivery_location: location
    status: str
    is_emergency: bool
