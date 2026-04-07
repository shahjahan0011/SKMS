import pytest
from fastapi import HTTPException
from app.services import rating_service


class TestCreateRatingValidation:
    """Test rating creation with validation"""
    
    def test_create_rating_success(self, monkeypatch):
        """Test successful rating creation"""
        order = {
            "order_id": "o1",
            "username": "jahan",
            "restaurant_id": "rest_1",
            "status": "delivered",
        }
        
        monkeypatch.setattr(rating_service, "get_order_by_id", lambda x: order)
        monkeypatch.setattr(rating_service, "get_rating_by_order", lambda x: None)
        monkeypatch.setattr(rating_service, "save_rating", lambda x: x)
        
        result = rating_service.create_rating(
            order_id="o1",
            restaurant_id="rest_1",
            username="jahan",
            score=5,
            comment="Great food!"
        )
        
        assert result["score"] == "5"
        assert result["comment"] == "Great food!"
        assert result["restaurant_id"] == "rest_1"
    
    
    def test_create_rating_order_not_found(self, monkeypatch):
        """Fault: Order doesn't exist"""
        monkeypatch.setattr(rating_service, "get_order_by_id", lambda x: None)
        
        with pytest.raises(HTTPException) as exc:
            rating_service.create_rating(
                order_id="bad_order",
                restaurant_id="rest_1",
                username="jahan",
                score=5
            )
        
        assert exc.value.status_code == 404


class TestOrderStatusValidation:
    """Equivalence Partitioning: Test status validation"""
    
    @pytest.mark.parametrize("status,can_rate", [
        ("pending", False),
        ("preparing", False),
        ("in-transit", False),
        ("delivered", True),
        ("cancelled", False),
    ])
    def test_only_delivered_orders_can_be_rated(self, status, can_rate, monkeypatch):
        """Test: Only delivered orders can be rated"""
        order = {
            "order_id": "o1",
            "username": "jahan",
            "restaurant_id": "rest_1",
            "status": status,
        }
        
        monkeypatch.setattr(rating_service, "get_order_by_id", lambda x: order)
        monkeypatch.setattr(rating_service, "get_rating_by_order", lambda x: None)
        
        if can_rate:
            monkeypatch.setattr(rating_service, "save_rating", lambda x: x)
            result = rating_service.create_rating(
                order_id="o1",
                restaurant_id="rest_1",
                username="jahan",
                score=5
            )
            assert result["score"] == "5"
        else:
            with pytest.raises(HTTPException) as exc:
                rating_service.create_rating(
                    order_id="o1",
                    restaurant_id="rest_1",
                    username="jahan",
                    score=5
                )
            assert exc.value.status_code == 400
            assert "delivered" in exc.value.detail.lower()


class TestRatingScoreValidation:
    """Boundary Testing: Rating scores 1-5"""
    
    @pytest.mark.parametrize("score,valid", [
        (0, False),      # Below range
        (1, True),       # Min valid
        (3, True),       # Middle
        (5, True),       # Max valid
        (6, False),      # Above range
        (-1, False),     # Negative
        (10, False),     # Way above
    ])
    def test_rating_score_boundaries(self, score, valid, monkeypatch):
        """Boundary: Test score boundaries 1-5"""
        order = {
            "order_id": "o1",
            "username": "jahan",
            "restaurant_id": "rest_1",
            "status": "delivered",
        }
        
        monkeypatch.setattr(rating_service, "get_order_by_id", lambda x: order)
        monkeypatch.setattr(rating_service, "get_rating_by_order", lambda x: None)
        
        if valid:
            monkeypatch.setattr(rating_service, "save_rating", lambda x: x)
            result = rating_service.create_rating(
                order_id="o1",
                restaurant_id="rest_1",
                username="jahan",
                score=score
            )
            assert result["score"] == str(score)
        else:
            with pytest.raises(HTTPException) as exc:
                rating_service.create_rating(
                    order_id="o1",
                    restaurant_id="rest_1",
                    username="jahan",
                    score=score
                )
            assert exc.value.status_code == 400


class TestAlreadyRatedValidation:
    """Test: Order can only be rated once"""
    
    def test_order_already_rated(self, monkeypatch):
        """Fault: Order already has a rating"""
        order = {
            "order_id": "o1",
            "username": "jahan",
            "restaurant_id": "rest_1",
            "status": "delivered",
        }
        
        existing_rating = {"rating_id": "r1", "order_id": "o1"}
        
        monkeypatch.setattr(rating_service, "get_order_by_id", lambda x: order)
        monkeypatch.setattr(rating_service, "get_rating_by_order", lambda x: existing_rating)
        
        with pytest.raises(HTTPException) as exc:
            rating_service.create_rating(
                order_id="o1",
                restaurant_id="rest_1",
                username="jahan",
                score=5
            )
        
        assert exc.value.status_code == 409
        assert "already been rated" in exc.value.detail


class TestOwnershipValidation:
    """Test: Users can only rate their own orders"""
    
    def test_user_rating_different_user_order(self, monkeypatch):
        """Fault: Trying to rate someone else's order"""
        order = {
            "order_id": "o1",
            "username": "john",  # Different user!
            "restaurant_id": "rest_1",
            "status": "delivered",
        }
        
        monkeypatch.setattr(rating_service, "get_order_by_id", lambda x: order)
        monkeypatch.setattr(rating_service, "get_rating_by_order", lambda x: None)
        
        with pytest.raises(HTTPException) as exc:
            rating_service.create_rating(
                order_id="o1",
                restaurant_id="rest_1",
                username="jahan",  # Different user
                score=5
            )
        
        assert exc.value.status_code == 403
        assert "own orders" in exc.value.detail


class TestRestaurantRatingStats:
    """Test rating statistics calculation"""
    
    def test_calculate_average_rating(self, monkeypatch):
        """Test: Average rating calculation"""
        ratings = [
            {"rating_id": "r1", "restaurant_id": "rest_1", "score": "5"},
            {"rating_id": "r2", "restaurant_id": "rest_1", "score": "4"},
            {"rating_id": "r3", "restaurant_id": "rest_1", "score": "3"},
        ]
        
        monkeypatch.setattr(rating_service, "get_ratings_by_restaurant", lambda x: ratings)
        
        stats = rating_service.get_restaurant_rating_stats("rest_1")
        
        assert stats["average_rating"] == 4.0  # (5+4+3)/3
        assert stats["total_ratings"] == 3
        assert stats["rating_breakdown"][5] == 1
        assert stats["rating_breakdown"][4] == 1
        assert stats["rating_breakdown"][3] == 1
    
    
    def test_no_ratings_returns_zeros(self, monkeypatch):
        """Test: Restaurant with no ratings"""
        monkeypatch.setattr(rating_service, "get_ratings_by_restaurant", lambda x: [])
        
        stats = rating_service.get_restaurant_rating_stats("rest_1")
        
        assert stats["average_rating"] == 0.0
        assert stats["total_ratings"] == 0
        assert all(count == 0 for count in stats["rating_breakdown"].values())