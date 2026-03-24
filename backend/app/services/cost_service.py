from fastapi import HTTPException

from app.storage.repositories.order_repository import get_menu_item_by_id


TAX_RATE = 0.05
DEFAULT_DELIVERY_FEE = 4.99
MINIMUM_ORDER_FOR_FREE_DELIVERY = 20.0


def _safe_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def calculate_base_cost(items: list[dict]) -> float:
    base_cost = 0.0

    for item in items:
        menu_item = get_menu_item_by_id(item["id"])
        if menu_item is None:
            raise HTTPException(status_code=404, detail=f"Menu item not found: {item['id']}")

        price = _safe_float(menu_item.get("price"))
        quantity = item["quantity"]
        base_cost += price * quantity

    return round(base_cost, 2)


def calculate_tax(base_cost: float) -> float:
    return round(base_cost * TAX_RATE, 2)


def calculate_delivery_fee(base_cost: float, is_premium: bool = False) -> float:
    if is_premium:
        return 0.0
    if base_cost >= MINIMUM_ORDER_FOR_FREE_DELIVERY:
        return 0.0
    return DEFAULT_DELIVERY_FEE


def calculate_total_breakdown(items: list[dict], is_premium: bool = False) -> dict:
    base_cost = calculate_base_cost(items)
    tax = calculate_tax(base_cost)
    delivery_fee = calculate_delivery_fee(base_cost, is_premium)
    total = round(base_cost + tax + delivery_fee, 2)

    return {
        "base_cost": base_cost,
        "tax": tax,
        "delivery_fee": delivery_fee,
        "total": total,
    }