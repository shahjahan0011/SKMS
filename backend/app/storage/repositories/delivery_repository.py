"""Delivery Repository"""

import csv

class delivery_repository:
    """Stores and retrieves delivery data"""

    def __init__(self):
        self.file_path = "data/deliveries.csv"

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
            fields = ["order_id", "restaurant_id", "user_id", "user_name", "status", "is_emergency"]
            writer = csv.DictWriter(file, fields=fields)

            writer.writeheader()
            writer.writerows(deliveries)
                