from pydantic import BaseModel
from typing import List
from app.schemas.menu_item import MenuItem


class Menu(BaseModel):
    """
    Menu Entity
    """

    menu_id: int
    items: List[MenuItem]