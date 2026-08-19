from fastapi import APIRouter, status, Response
from backend.app.core.database import verify_db_connection
from backend.app.core.redis import verify_redis_connection

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", status_code=status.HTTP_200_OK)
async def check_health(response: Response):
    """
    Checks the health of the FastAPI application and its key dependencies.
    Returns details on PostgreSQL and Redis status.
    """
    db_ok = await verify_db_connection()
    redis_ok = await verify_redis_connection()
    
    is_healthy = db_ok and redis_ok
    
    status_text = "healthy" if is_healthy else "unhealthy"
    if not is_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
    return {
        "status": status_text,
        "services": {
            "database": "online" if db_ok else "offline",
            "redis": "online" if redis_ok else "offline"
        }
    }
