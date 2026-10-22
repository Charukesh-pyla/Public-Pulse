# Models package — import all models here so Alembic can auto-detect them
from backend.app.core.database import Base

from backend.app.models.user import User
from backend.app.models.category import Category
from backend.app.models.problem import Problem
from backend.app.models.vote import Vote
from backend.app.models.evidence import Evidence

__all__ = ["Base", "User", "Category", "Problem", "Vote", "Evidence"]
