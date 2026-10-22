from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    """Schema for creating a category (admin/seed use)."""
    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=100)
    icon: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r"^#[0-9a-fA-F]{6}$")


class CategoryResponse(BaseModel):
    """Category returned in API responses."""
    id: UUID
    name: str
    slug: str
    icon: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None

    class Config:
        from_attributes = True
