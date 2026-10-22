from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Schema for creating a new user (or mock user during Phase 2)."""
    display_name: str = Field(..., min_length=2, max_length=100)
    supabase_id: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    """Public user profile returned in API responses."""
    id: UUID
    display_name: str
    avatar_url: Optional[str] = None
    reputation: int = 0
    is_moderator: bool = False
    created_at: datetime

    class Config:
        from_attributes = True
