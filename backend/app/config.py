import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "StockPulse API"
    app_env: str = os.getenv("APP_ENV", "development")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://stockpulse:stockpulse@localhost:5432/stockpulse"
    )
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
