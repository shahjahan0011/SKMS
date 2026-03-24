from fastapi import APIRouter

from app.schemas.cost_schema import CostPreviewRequest
from app.services.cost_service import (
    calculate_base_cost,
    calculate_tax,
    calculate_total_breakdown,
)
router = APIRouter(tags=["Cost"])


@router.post("/preview/base")
def preview_base_cost(payload: CostPreviewRequest):
    items = [{"id": item.id, "quantity": item.quantity} for item in payload.items]
    base_cost = calculate_base_cost(items)

    return {
        "base_cost": base_cost
    }


@router.post("/preview/tax")
def preview_cost_with_tax(payload: CostPreviewRequest):
    items = [{"id": item.id, "quantity": item.quantity} for item in payload.items]
    base_cost = calculate_base_cost(items)
    tax = calculate_tax(base_cost)

    return {
        "base_cost": base_cost,
        "tax": tax,
        "base_cost_with_tax": round(base_cost + tax, 2)
    }


@router.post("/preview/full")
def preview_full_cost(payload: CostPreviewRequest):
    items = [{"id": item.id, "quantity": item.quantity} for item in payload.items]

    return calculate_total_breakdown(
        items=items,
        is_premium=payload.is_premium,
    )