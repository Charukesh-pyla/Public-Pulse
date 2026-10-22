import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


class Vote(Base):
    """
    Tracks which user voted on which problem.
    One vote per user per problem, enforced by a unique constraint.
    """
    __tablename__ = "votes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user = relationship("User", back_populates="votes")
    problem = relationship("Problem", back_populates="votes")

    # Enforce one vote per user per problem
    __table_args__ = (
        UniqueConstraint("user_id", "problem_id", name="uq_user_problem_vote"),
    )

    def __repr__(self):
        return f"<Vote user={self.user_id} problem={self.problem_id}>"
