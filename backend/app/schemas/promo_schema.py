"""Promo Code Schema"""

from pydantic import BaseModel
from typing import Optional


class PromoCreate(BaseModel):
    """Schema used to create a promo code"""
    code: str
    discount_percent: int
    max_uses: int = 0  # 0 means unlimited


class PromoApply(BaseModel):
    """Schema used to apply a promo code to an order total"""
    code: str
    order_total: float


class PromoResponse(BaseModel):
    """Schema returned for promo code data"""
    code: str
    discount_percent: int
    max_uses: int
    times_used: int
    active: bool
    created_at: str


class PromoApplyResponse(BaseModel):
    """Schema returned after applying a promo code"""
    code: str
    discount_percent: int
    original_total: float
    discount_amount: float
    final_total: float