"""Delivery Services"""

from app.storage.repositories.delivery_repository import delivery_repository

class delivery_services:
    """
    Service for Delivery Management
    """

    def __init__(self):
        self.repo = delivery_repository()

    
    def get_all_deliveries(self):
        """returns all deliveries"""
        deliveries = self.repo.get_all_deliveries()
        return deliveries
    

    