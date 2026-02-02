"""
Configurações da aplicação
"""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = Field(default="postgresql://user:password@localhost:5432/chrono_tech_news")

    # OpenAI
    OPENAI_API_KEY: str = Field(default="")

    # App
    DEBUG: bool = Field(default=True)
    API_PORT: int = Field(default=8000)
    FRONTEND_URL: str = Field(default="http://localhost:5173")

    # Cron
    CRON_ENABLED: bool = Field(default=True)
    FETCH_NEWS_INTERVAL_MINUTES: int = Field(default=30)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
