from fastapi import HTTPException

from app.storage.repositories.order_repository import get_menu_item_by_id


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