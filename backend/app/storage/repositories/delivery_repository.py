"""Delivery Repository"""

import csv

class delivery_repository:
    """Stores and Retrieves Delivery Data"""

    def __init__(self):
        self.file_path = "backend/app/storage/data/deliveries.csv"
        self.location_file = "backend/app/storage/data/locations.csv"
        self.agent_file = "backend/app/storage/data/delivery_agents.csv"



    def _read_csv(self, file_path):
        """reads csv and returns list of dicts"""
        
        data = []
        with open(file_path, mode = "r", encoding = "utf-8", newline = "") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

        return data
    


    def _write_csv(self, file_path, data, fieldnames):
        """writes list of dicts to csv"""
        
        with open(file_path, mode = "w", encoding = "utf-8", newline = "") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)



    def get_all_deliveries(self):
        """returns all deliveries from csv """
        
        return self._read_csv(self.file_path)
        


    def get_delivery_by_order_id(self, order_id):
        """returns the order by order id"""
        
        deliveries = self._read_csv(self.file_path)
        for row in deliveries:
            if row["order_id"] == str(order_id):
                return row

        return None
    


    def create_delivery(self, delivery):
        """writes a new delivery into csv data"""

        with open(self.file_path, mode = "a", encoding = "utf-8", newline = "") as file:
            writer = csv.writer(file)

            writer.writerow([
                delivery["order_id"],
                delivery["restaurant_id"],
                delivery["user_id"],
                delivery["user_name"],
                delivery["delivery_location"].unit,
                delivery["delivery_location"].street,
                delivery["delivery_location"].postal_code,
                delivery["delivery_location"].province,
                delivery["delivery_location"].city,
                delivery["delivery_location"].country,
                delivery["status"],
                delivery["is_emergency"],
                delivery.get("agent_id", ""),
                delivery.get("agent_name", "")
            ])

    

    def update_delivery_status(self, order_id, new_status):
        """updates the delivery status for an order"""

        deliveries = self._read_csv(self.file_path)
        for row in deliveries:
            if row["order_id"] == str(order_id):
                row["status"] = new_status

        fields = [
            "order_id", "restaurant_id", "user_id", "user_name",
            "unit", "street", "postal_code", "province",
            "city", "country", "status", "is_emergency",
            "agent_id", "agent_name"
        ]

        self._write_csv(self.file_path, deliveries, fields)

    

    def get_user_deliveries(self, user_id):
        """returns all deliveries made by a user"""

        deliveries = self._read_csv(self.file_path)
        return [
            row for row in deliveries if row["user_id"] == str(user_id)
        ]   
    


    def save_location(self, location):
        """lets users save location"""

        with open(self.location_file, mode = "a", encoding = "utf-8", newline = "") as file:
            writer = csv.writer(file)

            writer.writerow([
                location["location_id"],
                location["user_id"],
                location["name"],
                location["unit"],
                location["street"],
                location["postal_code"],
                location["province"],
                location["city"],
                location["country"]
            ])
    


    def get_user_locations(self, user_id):
        """returns saved locations for a user based on their user id"""
        
        locations = self._read_csv(self.location_file)
        return [
            loc for loc in locations if loc["user_id"] == str(user_id)
        ]
    


    def delete_location(self, location_id):
        """lets user delete saved locations"""

        locations = self._read_csv(self.location_file)
        updated = [loc for loc in locations if loc["location_id"] != str(location_id)]
        fields = ["location_id","user_id","name","unit","street","postal_code","province","city","country"]
        
        self._write_csv(self.location_file, updated, fields)
    


    def get_all_locations(self):
        """returns all locations"""
        
        return self._read_csv(self.location_file)



    def get_available_agent(self):
        """returns first available agent"""

        with open(self.agent_file, mode = "r", encoding = "utf-8", newline = "") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["is_available"] == "True":
                    return row

        return None
    


    def set_agent_busy(self, agent_id):
        """sets agent as busy"""

        agents = self._read_csv(self.agent_file)
        for agent in agents:
            if agent["agent_id"] == str(agent_id):
                agent["is_available"] = "False"
        fields = ["agent_id","name","is_available"]
        
        self._write_csv(self.agent_file, agents, fields)



    def set_agent_available(self, agent_id):
        """sets agent back to available"""

        agents = self._read_csv(self.agent_file)
        for agent in agents:
            if agent["agent_id"] == str(agent_id):
                agent["is_available"] = "True"
        fields = ["agent_id","name","is_available"]
        
        self._write_csv(self.agent_file, agents, fields)
            