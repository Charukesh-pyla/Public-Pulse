"""
Temporary mock auth dependency for Phase 2.
Returns a mock user for all requests — will be replaced with real Supabase auth in Phase 3.
"""
import uuid
from typing import Optional
from fastapi import Header, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.models.user import User

# Fixed mock user ID used during development
MOCK_USER_ID = uuid.UUID("00000000-0000-4000-8000-000000000001")


async def get_current_user(
    x_user_id: Optional[str] = Header(None, description="Mock user ID header for dev"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Phase 2 mock auth: Looks up user by X-User-Id header.
    If no header provided, falls back to the default mock user.
    Auto-creates the mock user if it doesn't exist.
    """
    user_id = uuid.UUID(x_user_id) if x_user_id else MOCK_USER_ID

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        # Auto-create mock user
        user = User(
            id=user_id,
            display_name="Dev User" if user_id == MOCK_USER_ID else f"User {str(user_id)[:8]}",
            supabase_id=None,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user
