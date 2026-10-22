import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Text, Integer, DateTime, ForeignKey, Enum as SAEnum, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from pgvector.sqlalchemy import Vector
from backend.app.core.database import Base
import enum


# ── Enums ──────────────────────────────────────────────────────────────────

class ProblemType(str, enum.Enum):
    """community = citizen-reported, curated = editorially sourced national issues."""
    community = "community"
    curated = "curated"


class ProblemStatus(str, enum.Enum):
    draft = "draft"
    pending_review = "pending_review"
    published = "published"
    rejected = "rejected"
    resolved = "resolved"


class ProblemScope(str, enum.Enum):
    local = "local"
    city = "city"
    state = "state"
    national = "national"


# ── Model ──────────────────────────────────────────────────────────────────

class Problem(Base):
    """
    Core entity — a public problem reported by a citizen or curated by editors.
    Supports PostGIS location, pgvector embeddings, and denormalized vote/evidence counts.
    """
    __tablename__ = "problems"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    problem_type = Column(
        SAEnum(ProblemType, name="problem_type_enum", create_constraint=True),
        nullable=False,
        default=ProblemType.community,
    )
    status = Column(
        SAEnum(ProblemStatus, name="problem_status_enum", create_constraint=True),
        nullable=False,
        default=ProblemStatus.pending_review,
    )
    scope = Column(
        SAEnum(ProblemScope, name="problem_scope_enum", create_constraint=True),
        nullable=False,
        default=ProblemScope.local,
    )

    # Location
    location_name = Column(String(255), nullable=True)
    location = Column(Geometry("POINT", srid=4326), nullable=True)

    # AI embedding for duplicate detection (OpenAI text-embedding-3-small = 1536 dims)
    embedding = Column(Vector(1536), nullable=True)

    # Denormalized counters for fast sorting
    vote_count = Column(Integer, default=0, nullable=False, index=True)
    evidence_count = Column(Integer, default=0, nullable=False)

    # Foreign keys
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    author = relationship("User", back_populates="problems")
    category = relationship("Category", back_populates="problems")
    votes = relationship("Vote", back_populates="problem", cascade="all, delete-orphan", lazy="selectin")
    evidence = relationship("Evidence", back_populates="problem", cascade="all, delete-orphan", lazy="selectin")

    # Indexes for common queries
    __table_args__ = (
        Index("ix_problems_status_votes", "status", "vote_count"),
        Index("ix_problems_scope", "scope"),
        Index("ix_problems_created_at", "created_at"),
    )

    def __repr__(self):
        return f"<Problem '{self.title[:40]}' ({self.status.value})>"
