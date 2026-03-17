"""Menu Item Schema"""
from pydantic import BaseModel


class menu_item(BaseModel):
    """
    Menu Item Entity
    """

    menu_id: int
    item_id: int
    item_name: str
    price: float
