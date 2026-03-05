"""Menu Schema"""
from typing import List
from pydantic import BaseModel
from app.schemas.menu_item_schema import MenuItem


class Menu(BaseModel):
    """
    Menu Entity
    """

    menu_id: int
    items: List[MenuItem]
