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
    stock_count: int # updated for new M4 field
    is_available: bool # updated for new M4 field

class MenuInventoryUpdate(BaseModel):
    """
    When Admin updates the stock count of a menu item, this schema is used to add more inventory.
    """
    stock_count: int
