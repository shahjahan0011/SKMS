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
    