"""Router for delivery endpoints"""

from fastapi import APIRouter, HTTPException

from app.services.delivery_services import delivery_services
from app.schemas.delivery_schema import delivery
from app.schemas.location_schema import location

router = APIRouter()
delivery_service = delivery_services()


@router.get("/deliveries")
def get_all_deliveries():
    """get all deliveries"""

    return delivery_service.get_all_deliveries()



@router.get("/deliveries/{order_id}")
def get_delivery_by_order_id(order_id: int):
    """get delivery by order id"""

    try:
        return delivery_service.get_delivery_by_order_id(order_id)

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
    


@router.post("/deliveries")
def create_delivery(payload: delivery):
    """create a new delivery"""

    try:
        created_delivery = delivery_service.create_delivery(
            payload.order_id,
            payload.restaurant_id,
            payload.user_id,
            payload.user_name,
            payload.delivery_location,
            payload.status,
            payload.is_emergency
        )

        return created_delivery

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))



@router.patch("/deliveries/{order_id}/status")
def update_delivery_status(order_id: int, status: dict):
    """update delivery status"""


    try:
        updated = delivery_service.update_delivery_status(
            order_id,
            status["new_status"]
        )

        return updated

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))



@router.get("/deliveries/user/{user_id}")
def get_user_deliveries(user_id: int):
    """get deliveries for a user"""

    deliveries = delivery_service.get_user_deliveries(user_id)

    return deliveries



@router.post("/locations")
def save_location(user_id: int, name: str, payload: location):
    """save a new location"""

    location_data = {
        "user_id": user_id,
        "name": name,
        "unit": payload.unit,
        "street": payload.street,
        "postal_code": payload.postal_code,
        "province": payload.province,
        "city": payload.city,
        "country": payload.country
    }

    try:
        return delivery_service.save_location(location_data)

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    


@router.get("/locations/user/{user_id}")
def get_user_locations(user_id: int):
    """get saved locations for a user"""

    try:
        return delivery_service.get_user_locations(user_id)

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    


@router.delete("/locations/{location_id}")
def delete_location(location_id: int):
    """delete a saved location"""

    try:
        return delivery_service.delete_location(location_id)

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))



@router.get("/locations")
def get_all_locations():
    """get all saved locations"""

    return delivery_service.get_all_locations()



@router.get("/agents/available")
def get_available_agent():
    try:
        return delivery_service.get_available_agent()
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
