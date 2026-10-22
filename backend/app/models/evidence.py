import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
import enum


class FileType(str, enum.Enum):
    image = "image"
    video = "video"
    document = "document"
    link = "link"


class Evidence(Base):
    """
    Supporting evidence attached to a problem — photos, videos, documents, or links.
    Files are stored in Cloudflare R2; this table stores the URL reference.
    """
    __tablename__ = "evidence"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id"), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    file_url = Column(Text, nullable=False)
    file_type = Column(
        SAEnum(FileType, name="file_type_enum", create_constraint=True),
        nullable=False,
        default=FileType.image,
    )
    caption = Column(String(300), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    problem = relationship("Problem", back_populates="evidence")
    uploader = relationship("User", back_populates="evidence_uploads")

    def __repr__(self):
        return f"<Evidence {self.file_type.value} for problem={self.problem_id}>"
