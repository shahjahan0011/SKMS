"""Menu Item Schema"""
from typing import Optional

from pydantic import BaseModel


class MenuItem(BaseModel):
    """
    Menu Item Entity
    """

    menu_id: int
    item_id: int
    item_name: str
    price: float

class MenuItemDetail(MenuItem):
    """
    Expanded Schema for FR6: Detailed Menu Retrieval
    """
    description: Optional[str] = None
    is_available: bool = True

    class Config:
        from_attributes = True
