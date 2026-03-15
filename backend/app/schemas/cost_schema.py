from pydantic import BaseModel, Field
from typing import List


class CostItemRequest(BaseModel):
    id: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1)


class CostPreviewRequest(BaseModel):
    username: str = Field(..., min_length=1)
    items: List[CostItemRequest]