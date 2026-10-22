import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


class Category(Base):
    """
    Problem categories (e.g. Infrastructure, Healthcare, Education).
    Each problem belongs to one category.
    """
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    icon = Column(String(10), nullable=True)        # emoji icon
    description = Column(Text, nullable=True)
    color = Column(String(7), nullable=True)         # hex color like #ef4444

    # Relationships
    problems = relationship("Problem", back_populates="category", lazy="selectin")

    def __repr__(self):
        return f"<Category {self.name}>"
