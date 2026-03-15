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
    

    def get_delivery_by_order_id(self, order_id):
        """returns delivery for an order by order id"""

        delivery = self.repo.get_delivery_by_order_id(order_id)

        if delivery is None:
            raise ValueError("delivery not found")

        return delivery

    