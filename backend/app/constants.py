"""Constants and enums for the application"""
from enum import Enum


class UserRole(Enum):
    """Enum for user roles"""
    ADMIN = "admin"
    USER = "user"
    CUSTOMER = "customer"
    MANAGER = "manager"
    RESTAURANT_OWNER = "restaurant_owner"
    DELIVERY_DRIVER = "delivery_driver"


class NotificationEventType(Enum):
    """Enum for notification event types"""
    ORDER_CREATED = "order_created"
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    ORDER_STATUS_CHANGED = "order_status_changed"
    NEW_PAID_ORDER = "new_paid_order"

    # Added for M4 inventory alerts
    ITEM_SOLD_OUT = "inventory_sold_out"
    ITEM_LOW_STOCK = "inventory_low_stock"


class HTTPStatusCode:
    """HTTP status codes used in the application"""
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404


class UserCSVFields:
    """CSV field names for user storage"""
    USERNAME = "username"
    PASSWORD = "password"
    ROLE = "role"


class NotificationCSVFields:
    """CSV field names for notification storage"""
    ID = "id"
    USER_ID = "user_id"
    ROLE = "role"
    EVENT_TYPE = "event_type"
    EVENT_KEY = "event_key"
    MESSAGE = "message"
    ORDER_ID = "order_id"
    CREATED_AT = "created_at"


class ErrorMessages:
    """Centralized error messages"""
    # Auth errors
    USERNAME_REQUIRED = "Please enter a username"
    PASSWORD_REQUIRED = "Please enter password"
    USERNAME_EXISTS = "username already exists"
    INVALID_CREDENTIALS = "invalid username or password"
    USER_NOT_FOUND = "user does not exist"
    INSUFFICIENT_PERMISSIONS = "user does not have required role"



class PromoCSVFields:
    """CSV field names for promo code storage"""
    CODE = "code"
    DISCOUNT_PERCENT = "discount_percent"
    MAX_USES = "max_uses"
    TIMES_USED = "times_used"
    ACTIVE = "active"
    CREATED_AT = "created_at"


class PromoErrorMessages:
    """Error messages for promo code feature"""
    CODE_REQUIRED = "promo code is required"
    CODE_EXISTS = "promo code already exists"
    CODE_NOT_FOUND = "promo code does not exist"
    CODE_INACTIVE = "promo code is not active"
    CODE_USAGE_LIMIT_REACHED = "promo code has reached its usage limit"
    INVALID_DISCOUNT = "discount percent must be between 1 and 100"
    INVALID_MAX_USES = "max uses must be 0 (unlimited) or greater than 0"
    INVALID_ORDER_TOTAL = "order total must be greater than 0"