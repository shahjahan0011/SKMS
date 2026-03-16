"""Menu Schema"""
from typing import List
from pydantic import BaseModel
from app.schemas.menu_item_schema import menu_item


class menu(BaseModel):
    """
    Menu Entity
    """

    menu_id: int
    items: List[menu_item]
