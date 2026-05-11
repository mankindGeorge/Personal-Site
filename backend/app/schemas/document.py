from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DocumentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100)
    content: str = ""
    category: str = "blog"
    tags: List[str] = []
    order_index: int = 0
    parent_id: Optional[int] = None
    is_published: bool = True


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    order_index: Optional[int] = None
    parent_id: Optional[int] = None
    is_published: Optional[bool] = None


class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
