from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class VoteResponse(BaseModel):
    """Single vote record."""
    id: UUID
    user_id: UUID
    problem_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class VoteToggleResponse(BaseModel):
    """Response from the vote toggle endpoint."""
    voted: bool               # True if vote was cast, False if removed
    new_vote_count: int       # Updated total vote count for the problem
    message: str
