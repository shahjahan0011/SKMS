"""User's Favorites Repository"""
import csv
import os

class favorite_repository:

    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATA_DIR = os.path.join(BASE_DIR, "data")

        self.file_path = os.path.join(DATA_DIR, "favorites.csv")

        # create file if not exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode = "w", newline = "") as file:
                writer = csv.writer(file)
                writer.writerow(["user_id", "restaurant_id"])

    def get_all(self):
        data = []
        try:
            with open(self.file_path, mode = "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            return []
        return data
    
    def write_all(self, data):
        with open(self.file_path, mode = "w", newline = "") as file:
            writer = csv.DictWriter(file, fieldnames=["user_id", "restaurant_id"])
            writer.writeheader()
            writer.writerows(data)

    def add_favorite(self, user_id, restaurant_id):
        favorites = self.get_all()

        # check if already exists
        for fav in favorites:
            if fav["user_id"] == str(user_id) and fav["restaurant_id"] == str(restaurant_id):
                raise Exception("Already in favorites")

        favorites.append({
            "user_id": str(user_id),
            "restaurant_id": str(restaurant_id)
        })

        self.write_all(favorites)

    def remove_favorite(self, user_id, restaurant_id):
        favorites = self.get_all()

        new_data = []
        for fav in favorites:
            if not (fav["user_id"] == str(user_id) and fav["restaurant_id"] == str(restaurant_id)):
                new_data.append(fav)

        self.write_all(new_data)

    def get_user_favorites(self, user_id):
        favorites = self.get_all()

        result = []
        for fav in favorites:
            if fav["user_id"] == str(user_id):
                result.append(fav)

        return result


favorite_repository = favorite_repository()