from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AnnouncementBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = ""
    type: str = "info"
    priority: int = 0
    is_published: bool = True


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    type: Optional[str] = None
    priority: Optional[int] = None
    is_published: Optional[bool] = None


class AnnouncementResponse(AnnouncementBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
