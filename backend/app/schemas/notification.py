from pydantic import BaseModel
from typing import Optional

class NotificationCreateSchema(BaseModel):
    user_id: int
    type: str
    title: str
    content: str
    link: Optional[str] = None
    extra_data: Optional[dict] = None

class NotificationResponseSchema(BaseModel):
    id: int
    type: str
    title: str
    content: str
    link: Optional[str]
    is_read: bool
    created_at: str
    extra_data: Optional[dict]