import pytest
from app.storage.repositories.order_items_repository import (
    save_order_item,
    get_order_items,
    get_all_order_items,
    delete_order_items,
)


def test_save_order_item_success():
    """Test saving a single order item"""
    order_id = "test_order_1"
    item_id = "item_1"
    quantity = 2
    item_price = 15.50
    
    result = save_order_item(order_id, item_id, quantity, item_price)
    
    assert result["order_id"] == order_id
    assert result["item_id"] == item_id
    assert result["quantity"] == "2"
    assert result["item_price"] == "15.50"
    assert result["order_item_id"] is not None  # Should be a UUID


def test_get_order_items_success():
    """Test retrieving items for an order"""
    order_id = "test_order_2"
    
    # Save multiple items for same order
    save_order_item(order_id, "item_1", 1, 10.00)
    save_order_item(order_id, "item_2", 2, 15.00)
    
    items = get_order_items(order_id)
    
    assert len(items) == 2
    assert items[0]["item_id"] == "item_1"
    assert items[1]["item_id"] == "item_2"


def test_get_order_items_empty():
    """Test retrieving items for order with no items"""
    items = get_order_items("nonexistent_order")
    
    assert items == []


def test_get_order_items_isolated():
    """Test that get_order_items only returns items for specified order"""
    order_1 = "test_order_3"
    order_2 = "test_order_4"
    
    save_order_item(order_1, "item_1", 1, 10.00)
    save_order_item(order_2, "item_2", 1, 20.00)
    
    items_1 = get_order_items(order_1)
    items_2 = get_order_items(order_2)
    
    assert len(items_1) == 1
    assert len(items_2) == 1
    assert items_1[0]["item_id"] == "item_1"
    assert items_2[0]["item_id"] == "item_2"


def test_delete_order_items_success():
    """Test deleting items for an order"""
    order_to_delete = "test_order_5"
    order_to_keep = "test_order_6"
    
    save_order_item(order_to_delete, "item_1", 1, 10.00)
    save_order_item(order_to_keep, "item_2", 1, 20.00)
    
    # Verify both exist
    assert len(get_order_items(order_to_delete)) == 1
    assert len(get_order_items(order_to_keep)) == 1
    
    # Delete one order's items
    delete_order_items(order_to_delete)
    
    # Verify deletion
    assert len(get_order_items(order_to_delete)) == 0
    assert len(get_order_items(order_to_keep)) == 1


def test_delete_order_items_nonexistent():
    """Test deleting items for order that doesn't exist (should not fail)"""
    # Should not raise an error
    delete_order_items("nonexistent_order")
    
    # Should still be able to query
    assert get_order_items("nonexistent_order") == []


def test_get_all_order_items():
    """Test retrieving all items from all orders"""
    order_1 = "test_order_7"
    order_2 = "test_order_8"
    
    save_order_item(order_1, "item_1", 1, 10.00)
    save_order_item(order_1, "item_2", 1, 15.00)
    save_order_item(order_2, "item_3", 2, 20.00)
    
    all_items = get_all_order_items()
    
    # Should have at least 3 items (may have more from other tests)
    assert len(all_items) >= 3


def test_item_price_formatting():
    """Test that item prices are formatted correctly"""
    result = save_order_item("test_order_9", "item_1", 1, 10)
    
    assert result["item_price"] == "10.00"
    
    result2 = save_order_item("test_order_10", "item_2", 1, 10.5)
    
    assert result2["item_price"] == "10.50"


def test_quantity_string_conversion():
    """Test that quantity is stored as string"""
    result = save_order_item("test_order_11", "item_1", 5, 10.00)
    
    assert result["quantity"] == "5"
    assert isinstance(result["quantity"], str)