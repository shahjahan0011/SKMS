"""Router for delivery endpoints"""

from fastapi import APIRouter, HTTPException

from app.services.delivery_services import delivery_service
from app.storage.repositories.delivery_repository import delivery_repository

router = APIRouter()
"""Repo and services for delivery management"""
delivery_repository = delivery_repository()
delivery_service = delivery_service()


@router.get("/deliveries")
def get_all_deliveries():
    """get all deliveries"""

    return delivery_service.get_all_deliveries()


