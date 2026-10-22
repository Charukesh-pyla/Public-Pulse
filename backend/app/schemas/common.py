from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar("T")


class MessageResponse(BaseModel):
    """Generic message response for simple API confirmations."""
    message: str
    success: bool = True


class PaginatedResponse(BaseModel, Generic[T]):
    """Wrapper for paginated list responses."""
    items: List[T]
    total: int
    page: int
    per_page: int
    total_pages: int

    class Config:
        from_attributes = True
