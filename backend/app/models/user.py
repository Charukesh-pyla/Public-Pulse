import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


class User(Base):
    """
    Represents a registered citizen on the platform.
    Linked to Supabase Auth via supabase_id.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supabase_id = Column(String(255), unique=True, nullable=True, index=True)
    display_name = Column(String(100), nullable=False)
    avatar_url = Column(Text, nullable=True)
    reputation = Column(Integer, default=0, nullable=False)
    is_moderator = Column(Boolean, default=False, nullable=False)
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
    problems = relationship("Problem", back_populates="author", lazy="selectin")
    votes = relationship("Vote", back_populates="user", lazy="selectin")
    evidence_uploads = relationship("Evidence", back_populates="uploader", lazy="selectin")

    def __repr__(self):
        return f"<User {self.display_name} ({self.id})>"
