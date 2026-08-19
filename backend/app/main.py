from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.routers import health

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Public Priority Platform, managing problem reports, spatial queries, and AI duplicates.",
    version="0.1.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to the {settings.PROJECT_NAME}",
        "version": "0.1.0",
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
