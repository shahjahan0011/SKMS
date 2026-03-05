import csv

FILE_PATH = "app/storage/users.csv"

def register_user(username, password):
    with open(FILE_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([username, password])

def login_user(username, password):
    with open(FILE_PATH, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False
