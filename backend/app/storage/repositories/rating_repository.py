import csv
from pathlib import Path
from typing import List, Optional
from uuid import uuid4


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "ratings.csv"

FIELDNAMES = [
    "rating_id",
    "order_id",
    "restaurant_id",
    "username",
    "score",
    "comment",
    "created_at",
]


def _ensure_file_exists() -> None:
    """Ensure ratings.csv exists with headers."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def save_rating(rating_data: dict) -> dict:
    """Save a rating to CSV."""
    _ensure_file_exists()
    
    filtered_rating = {k: v for k, v in rating_data.items() if k in FIELDNAMES}
    
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(filtered_rating)
    
    return filtered_rating


def get_rating_by_id(rating_id: str) -> Optional[dict]:
    """Get a rating by ID."""
    rating_id = str(rating_id).strip()
    
    _ensure_file_exists()
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if not reader:
            return None
        for row in reader:
            if str(row.get("rating_id", "")).strip() == rating_id:
                return row
    return None


def get_all_ratings() -> List[dict]:
    """Get all ratings."""
    _ensure_file_exists()
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader) if reader else []


def get_ratings_by_restaurant(restaurant_id: str) -> List[dict]:
    """Get all ratings for a restaurant."""
    return [r for r in get_all_ratings() if r.get("restaurant_id") == restaurant_id]


def get_ratings_by_user(username: str) -> List[dict]:
    """Get all ratings by a user."""
    return [r for r in get_all_ratings() if r.get("username") == username]


def get_rating_by_order(order_id: str) -> Optional[dict]:
    """Get rating for a specific order (should be unique)."""
    for rating in get_all_ratings():
        if rating.get("order_id") == order_id:
            return rating
    return None


def update_rating(updated_rating: dict) -> Optional[dict]:
    """Update an existing rating."""
    ratings = get_all_ratings()
    updated = None

    for index, rating in enumerate(ratings):
        if rating.get("rating_id") == updated_rating.get("rating_id"):
            merged = {**rating, **updated_rating}
            filtered = {k: v for k, v in merged.items() if k in FIELDNAMES}
            ratings[index] = filtered
            updated = filtered
            break

    if updated is None:
        return None

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(ratings)

    return updated


def delete_rating(rating_id: str) -> bool:
    """Delete a rating."""
    ratings = get_all_ratings()
    initial_count = len(ratings)
    
    ratings = [r for r in ratings if r.get("rating_id") != rating_id]
    
    if len(ratings) == initial_count:
        return False  # Rating not found

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(ratings)

    return True