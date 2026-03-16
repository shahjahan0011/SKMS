"""Restaurant Schema"""

from pydantic import BaseModel


class restaurant(BaseModel):
    """
    Restaurant Entity
    """

    restaurant_id: int
    restaurant_name: str
    menu_id: int
