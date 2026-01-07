from pydantic_settings import BaseSettings
from typing import List, Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "CPC Backend"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/cpc_backend"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Discord
    DISCORD_WEBHOOK_URL: str = "https://discord.com/api/webhooks/1458519726182367304/lbuB73PRLYhKDcI8-S3xAIVUDmfS3UsbXS3MCh27jCTHIduZKwshMW6Bon1kBGDB9Vt2"

    class Config:
        case_sensitive = True

settings = Settings()
