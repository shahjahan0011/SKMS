from fastapi import APIRouter

from app.schemas.cost_schema import CostPreviewRequest
from app.services.cost_service import calculate_base_cost

router = APIRouter(prefix="/cost", tags=["cost"])


@router.post("/preview/base")
def preview_base_cost(payload: CostPreviewRequest):
    items = [{"id": item.id, "quantity": item.quantity} for item in payload.items]
    base_cost = calculate_base_cost(items)

    return {
        "base_cost": base_cost
    }