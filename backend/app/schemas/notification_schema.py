"""Notification Schema"""

from pydantic import BaseModel


class notification_create(BaseModel):
    """Schema used to create a notification"""

    user_id: str
    role: str
    event_type: str
    event_key: str
    message: str
    order_id: str


class notification_response(BaseModel):
    """Schema returned for notification data"""

    id: str
    user_id: str
    role: str
    event_type: str
    event_key: str
    message: str
    order_id: str
    created_at: str