import redis.asyncio as redis
from backend.app.core.config import settings

# Initialize asynchronous Redis connection pool
redis_client = redis.from_url(
    settings.REDIS_URL, 
    decode_responses=True,
    socket_timeout=5.0
)

async def verify_redis_connection() -> bool:
    """Verifies that Redis is reachable and active."""
    try:
        return await redis_client.ping()
    except Exception:
        return False
