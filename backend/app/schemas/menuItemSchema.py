from pydantic import BaseModel


class MenuItem(BaseModel):
    """
    Menu Item Entity
    """

    menu_id: int
    item_id: int
    item_name: str
    price: float