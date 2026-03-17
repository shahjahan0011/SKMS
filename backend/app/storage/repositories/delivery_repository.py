"""Delivery Repository"""

import csv

class delivery_repository:
    """Stores and retrieves delivery data"""

    def __init__(self):
        self.file_path = "backend/app/storage/data/deliveries.csv"
        self.location_file = "backend/app/storage/data/locations.csv"

    def get_all_deliveries(self):
        """returns all deliveries from csv """

        deliveries = []

        with open(self.file_path, mode = "r", encoding = "utf-8", newline = "") as file: 
            reader = csv.DictReader(file)

            for row in reader:
                deliveries.append(row)

        return deliveries
        

    def get_delivery_by_order_id(self, order_id):
        """returns the order by order id"""

        with open(self.file_path, mode = "r", encoding = "utf-8", newline = "") as file: 
            reader = csv.DictReader(file)

            for row in reader:
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
                delivery["is_emergency"]
            ])

    
    def update_delivery_status(self, order_id, new_status):
        """updates the delivery status for an order"""

        deliveries = []

        with open(self.file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["order_id"] == str(order_id):
                    row["status"] = new_status

                deliveries.append(row)

        with open(self.file_path, mode="w", encoding="utf-8", newline="") as file:
            fields = ["order_id", "restaurant_id", "user_id", "user_name", "unit", "street", "postal_code", "province", "city", "country", "status", "is_emergency"]
            writer = csv.DictWriter(file, fieldnames=fields)

            writer.writeheader()
            writer.writerows(deliveries)

    
    def get_user_deliveries(self, user_id):
        """returns all deliveries made by a user"""

        user_deliveries = []

        with open(self.file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["user_id"] == str(user_id):
                    user_deliveries.append(row)

        return user_deliveries    
    

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

        locations = []

        with open(self.location_file, mode = "r", encoding = "utf-8", newline = "") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["user_id"] == str(user_id):
                    locations.append(row)

        return locations
    

    def delete_location(self, location_id):
        """lets user delete saved locations"""

        locations = []

        with open(self.location_file, mode = "r", encoding = "utf-8", newline = "") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["location_id"] != str(location_id):
                    locations.append(row)

        with open(self.location_file, mode = "w", encoding = "utf-8", newline = "") as file:
            fields = ["location_id","user_id","name","unit","street","postal_code","province","city","country"]
            writer = csv.DictWriter(file, fieldnames=fields)

            writer.writeheader()
            writer.writerows(locations)
    

    def get_all_locations(self):
        """returns all locations"""

        locations = []

        with open(self.location_file, mode = "r", encoding = "utf-8", newline = "") as file:
            reader = csv.DictReader(file)

            for row in reader:
                locations.append(row)

        return locations
