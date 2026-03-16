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
    

    def create_delivery(self, order_id, restaurant_id, user_id, user_name, delivery_location, status, is_emergency):
        """creates a new delivery"""

        existing = self.repo.get_delivery_by_order_id(order_id)

        if existing:
            raise ValueError("delivery already exists for this order")

        delivery_data = {
            "order_id": order_id,
            "restaurant_id": restaurant_id,
            "user_id": user_id,
            "user_name": user_name,
            "delivery_location": delivery_location,
            "status": status,
            "is_emergency": is_emergency
        }

        self.repo.create_delivery(delivery_data)

        return delivery_data
    

    def update_delivery_status(self, order_id, new_status):
        """updates status of a delivery"""

        delivery = self.repo.get_delivery_by_order_id(order_id)

        if delivery is None:
            raise ValueError("delivery not found")

        self.repo.update_delivery_status(order_id, new_status)

        return {
            "order_id": order_id,
            "new_status": new_status
        }
    

    def get_user_deliveries(self, user_id):
        """returns deliveries for a user"""

        deliveries = self.repo.get_user_deliveries(user_id)

        return deliveries
    