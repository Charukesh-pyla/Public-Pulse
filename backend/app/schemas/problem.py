from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from backend.app.models.problem import ProblemType, ProblemStatus, ProblemScope
from backend.app.schemas.category import CategoryResponse
from backend.app.schemas.user import UserResponse


class ProblemCreate(BaseModel):
    """Schema for submitting a new problem."""
    title: str = Field(..., min_length=10, max_length=200)
    description: str = Field(..., min_length=20, max_length=5000)
    problem_type: ProblemType = ProblemType.community
    scope: ProblemScope = ProblemScope.local
    location_name: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    category_id: Optional[UUID] = None
    tags: Optional[List[str]] = None


class ProblemUpdate(BaseModel):
    """Schema for updating an existing problem (partial update)."""
    title: Optional[str] = Field(None, min_length=10, max_length=200)
    description: Optional[str] = Field(None, min_length=20, max_length=5000)
    scope: Optional[ProblemScope] = None
    location_name: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    category_id: Optional[UUID] = None
    status: Optional[ProblemStatus] = None


class ProblemResponse(BaseModel):
    """Full problem detail returned in API responses."""
    id: UUID
    title: str
    description: str
    problem_type: ProblemType
    status: ProblemStatus
    scope: ProblemScope
    location_name: Optional[str] = None
    vote_count: int = 0
    evidence_count: int = 0
    author: UserResponse
    category: Optional[CategoryResponse] = None
    has_voted: bool = False  # populated per-request based on current user
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProblemListResponse(BaseModel):
    """Paginated list of problems."""
    items: List[ProblemResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

    class Config:
        from_attributes = True
