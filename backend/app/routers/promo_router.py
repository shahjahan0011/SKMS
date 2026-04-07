"""endpoints for promo codes"""
from fastapi import APIRouter, HTTPException, Query, Depends

from app.schemas.promo_schema import PromoCreate, PromoApply
from app.services.promo_service import PromoService
from app.services.auth_service import AuthService
from app.dependencies import get_promo_service, get_auth_service
from app.constants import HTTPStatusCode, UserRole

router = APIRouter(prefix="/promos", tags=["Promo Codes"])


def _require_admin(username: str, auth: AuthService):
    """helper to gate admin-only endpoints"""
    try:
        auth.check_role(username, UserRole.ADMIN.value)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatusCode.NOT_FOUND,
            detail=str(error)
        ) from error
    except PermissionError as error:
        raise HTTPException(
            status_code=HTTPStatusCode.FORBIDDEN,
            detail=str(error)
        ) from error


@router.post("/")
def create_promo(
    promo: PromoCreate,
    username: str = Query(...),
    auth: AuthService = Depends(get_auth_service),
    service: PromoService = Depends(get_promo_service)
):
    """create a new promo code (admin only)"""
    _require_admin(username, auth)

    try:
        return service.create_promo(promo.code, promo.discount_percent, promo.max_uses)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatusCode.BAD_REQUEST,
            detail=str(error)
        ) from error


@router.get("/")
def list_promos(
    username: str = Query(...),
    auth: AuthService = Depends(get_auth_service),
    service: PromoService = Depends(get_promo_service)
):
    """list all promo codes (admin only)"""
    _require_admin(username, auth)
    return {"promos": service.get_all_promos()}


@router.get("/{code}")
def get_promo(
    code: str,
    service: PromoService = Depends(get_promo_service)
):
    """get a single promo code"""
    try:
        return service.get_promo(code)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatusCode.NOT_FOUND,
            detail=str(error)
        ) from error


@router.delete("/{code}")
def delete_promo(
    code: str,
    username: str = Query(...),
    auth: AuthService = Depends(get_auth_service),
    service: PromoService = Depends(get_promo_service)
):
    """delete a promo code (admin only)"""
    _require_admin(username, auth)

    try:
        return service.delete_promo(code)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatusCode.NOT_FOUND,
            detail=str(error)
        ) from error


@router.patch("/{code}/active")
def toggle_promo(
    code: str,
    active: bool = Query(...),
    username: str = Query(...),
    auth: AuthService = Depends(get_auth_service),
    service: PromoService = Depends(get_promo_service)
):
    """activate or deactivate a promo code (admin only)"""
    _require_admin(username, auth)

    try:
        return service.toggle_promo_active(code, active)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatusCode.NOT_FOUND,
            detail=str(error)
        ) from error


@router.post("/apply")
def apply_promo(
    payload: PromoApply,
    service: PromoService = Depends(get_promo_service)
):
    """validate a promo code and calculate the discount for an order total"""
    try:
        return service.apply_promo(payload.code, payload.order_total)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatusCode.BAD_REQUEST,
            detail=str(error)
        ) from error