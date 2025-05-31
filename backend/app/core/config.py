import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, HttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Project metadata
    PROJECT_NAME: str = "Kite Trading App"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    TESTING: bool = False
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change this in production
    JWT_SECRET: str = "your-jwt-secret-here"  # Change this in production
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "kiteapp"
    POSTGRES_PORT: str = "5432"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = "postgresql://postgres:postgres@localhost:5432/kiteapp"
    
    @property
    def get_database_url(self) -> str:
        """Get database URL from SQLALCHEMY_DATABASE_URI or generate from environment variables."""
        if self.SQLALCHEMY_DATABASE_URI:
            return str(self.SQLALCHEMY_DATABASE_URI)
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Kite Connect
    KITE_API_KEY: str = "14omewt7sjd5v739"
    KITE_API_SECRET: str = "ddyd72svfi7qdvehyrfvn5d25l738o9p"
    KITE_REDIRECT_URI: str = "http://localhost:3000/auth/callback"
    
    # Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    
    # Trading
    MAX_POSITION_SIZE: float = 100000.0  # ₹1L
    MAX_DAILY_LOSS: float = 5000.0  # ₹5K
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # API
    API_PREFIX: str = "/api"
    OPENAPI_URL: Optional[str] = "/openapi.json"
    
    # Rate limiting
    RATE_LIMIT: str = "100/minute"
    
    # Security headers
    SECURE_HSTS_SECONDS: int = 60 * 60 * 24 * 365  # 1 year
    SECURE_CONTENT_TYPE_NOSNIFF: bool = True
    SECURE_BROWSER_XSS_FILTER: bool = True
    SECURE_SSL_REDIRECT: bool = False
    SESSION_COOKIE_SECURE: bool = True
    CSRF_COOKIE_SECURE: bool = True
    
    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # Redis (for rate limiting, caching, etc.)
    REDIS_URL: Optional[str] = None
    
    # Sentry
    SENTRY_DSN: str = ""
    
    # Model Config
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")
    
    @property
    def DATABASE_URI(self) -> str:
        """Get the database URI."""
        if self.SQLALCHEMY_DATABASE_URI:
            return str(self.SQLALCHEMY_DATABASE_URI)
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def SYNC_DATABASE_URI(self) -> str:
        """Get the synchronous database URI (for migrations, etc.)."""
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def CORS_ORIGIN_LIST(self) -> list[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @field_validator("SENTRY_DSN", mode="before")
    @classmethod
    def assemble_sentry_dsn(cls, v: Optional[str], info: Any) -> Optional[str]:
        """Assemble Sentry DSN."""
        if isinstance(v, str):
            return v
        return None
    
    @field_validator("EMAILS_FROM_EMAIL")
    @classmethod
    def get_emails_from_email(cls, v: Optional[str], info: Any) -> Optional[str]:
        """Get the default email address for sending emails."""
        if not v:
            return f"noreply@{info.data.get('DOMAIN', 'localhost')}"
        return v
    
    @field_validator("EMAILS_FROM_NAME")
    @classmethod
    def get_emails_from_name(cls, v: Optional[str], info: Any) -> str:
        """Get the default name for sending emails."""
        if not v:
            return info.data.get("PROJECT_NAME")
        return v


# Load settings
settings = Settings()

# Set up logging
logging_config: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
        "console": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": "logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "root": {
        "handlers": ["console", "file"] if settings.ENVIRONMENT != "test" else ["console"],
        "level": settings.LOG_LEVEL,
    },
    "loggers": {
        "uvicorn": {"level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "sqlalchemy": {"level": "WARNING"},
        "aiosqlite": {"level": "WARNING"},
    },
}

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
import logging.config
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

# Log configuration at startup
if settings.ENVIRONMENT != "test":
    logger.info("Starting application with settings:")
    for key, value in settings.model_dump().items():
        if any(sensitive in key.lower() for sensitive in ["key", "secret", "password", "token"]):
            value = "***" if value else ""
        logger.info(f"  {key}: {value}")