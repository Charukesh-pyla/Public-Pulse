import json
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Public Priority Platform API"
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str
    
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Converts postgresql:// to postgresql+asyncpg:// for async drivers."""
        url = self.DATABASE_URL
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgres://"):
            # Handle Supabase style postgres:// URLs
            return url.replace("postgres://", "postgresql+asyncpg://", 1)
        return url

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # OpenAI
    OPENAI_API_KEY: str = "mock-key-for-now"

    # Supabase Auth
    SUPABASE_URL: str = "https://mock.supabase.co"
    SUPABASE_ANON_KEY: str = "mock-anon-key"
    SUPABASE_SERVICE_ROLE_KEY: str = "mock-service-role-key"

    # CORS Origins
    BACKEND_CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str) and v.startswith("["):
            try:
                return json.loads(v)
            except Exception:
                return [v]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
