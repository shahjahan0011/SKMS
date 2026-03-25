"""Delivery Services"""

from app.storage.repositories.delivery_repository import delivery_repository

class delivery_services:
    """
    Service for Delivery Management
    """

    def __init__(self):
        self.repo = delivery_repository()

    status_set = [
        "placed",
        "preparing",
        "picked up",
        "on the way",
        "delivered"
    ]



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
    


    def _validate_delivery(self, order_id, status):
        """checks if a delivery is valid"""
        if status not in self.status_set:
            raise ValueError("invalid delivery status")

        if not order_id:
            raise ValueError("order id required")

        existing = self.repo.get_delivery_by_order_id(order_id)

        if existing:
            raise ValueError("delivery already exists for this order")
        


    def _assign_agent(self):
        """assigns a delivery agent"""
        agent = self.repo.get_available_agent()

        if agent is None:
            raise ValueError("no delivery agents available")

        self.repo.set_agent_busy(agent["agent_id"])

        return agent


    def delivery_data(self, order_id, restaurant_id, user_id, user_name, delivery_location, status, is_emergency, agent):
        """builds delivery data"""
        return {
            "order_id": order_id,
            "restaurant_id": restaurant_id,
            "user_id": user_id,
            "user_name": user_name,
            "delivery_location": delivery_location,
            "status": status,
            "is_emergency": is_emergency,
            "agent_id": agent["agent_id"],
            "agent_name": agent["name"]
        }



    def create_delivery(self, order_id, restaurant_id, user_id, user_name, delivery_location, status, is_emergency):
        """creates a new delivery"""
        
        self._validate_delivery(order_id, status)        
        agent = self._assign_agent()
        data = self.delivery_data(
            order_id,
            restaurant_id,
            user_id,
            user_name,
            delivery_location,
            status,
            is_emergency,
            agent
        )

        self.repo.create_delivery(data)

        return data
    


    def update_delivery_status(self, order_id, new_status):
        """updates status of a delivery"""

        delivery = self.repo.get_delivery_by_order_id(order_id)

        if new_status not in self.status_set:
            raise ValueError("invalid delivery status")
        
        if delivery is None:
            raise ValueError("delivery not found")

        self.repo.update_delivery_status(order_id, new_status)

        updated_delivery = self.repo.get_delivery_by_order_id(order_id)

        if new_status == "delivered":
            if updated_delivery.get("agent_id"):
                self.repo.set_agent_available(updated_delivery["agent_id"])
        return {
            "order_id": order_id,
            "new_status": new_status
        }
    


    def get_user_deliveries(self, user_id):
        """returns deliveries for a user"""

        deliveries = self.repo.get_user_deliveries(user_id)

        return deliveries
    


    def save_location(self, location):
        """saves location for user"""

        if not location["user_id"]:
            raise ValueError("user id required")

        if not location["name"]:
            raise ValueError("location name required")

        if not location["street"] or not location["postal_code"] or not location["city"] or not location["country"]:
            raise ValueError("location fields cannot be empty")

        if location["unit"] is None:
            raise ValueError("unit is required")

        all_locations = self.repo.get_all_locations()
        location["location_id"] = len(all_locations) + 1

        self.repo.save_location(location)

        return location
    


    def get_user_locations(self, user_id):
        """returns saved locations for a user"""
        
        if not user_id:
            raise ValueError("user id required")
        
        locations = self.repo.get_user_locations(user_id)

        return locations
    


    def delete_location(self, location_id):
        """deletes a saved location"""
        
        if not location_id:
            raise ValueError("location id required")

        locations = self.repo.get_all_locations()
        found = False
        for loc in locations:
            if loc["location_id"] == str(location_id):
                found = True
                break

        if not found:
            raise ValueError("location not found")
        self.repo.delete_location(location_id)

        return {"message": "location deleted"}
    


    def get_all_locations(self):
        """returns all saved locations"""

        locations = self.repo.get_all_locations()

        return locations
    