from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from backend.app.core.config import settings

# echo=True is helpful for development to see raw SQL logs
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    future=True
)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    """Dependency to get async DB session in route handlers."""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
            
async def verify_db_connection() -> bool:
    """Verifies that the database is reachable and active."""
    try:
        from sqlalchemy import text
        async with SessionLocal() as session:
            # Query to verify connection and check extensions
            result = await session.execute(text("SELECT 1;"))
            return result.scalar() == 1
    except Exception:
        return False
