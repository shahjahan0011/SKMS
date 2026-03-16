"""Location Schema"""
from pydantic import BaseModel

class location(BaseModel):
    """
    Location Entity
    """

    unit: int
    street : str
    postal_code: str
    province: str
    city: str
    country: str