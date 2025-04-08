from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, HttpUrl, EmailStr
from typing import Optional


class Settings(BaseSettings):
    """Application settings using Pydantic."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    # Application Settings
    APP_NAME: str = "RAG Application"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]
    REQUEST_ID_HEADER: str = "X-Request-ID"
    
    # Security
    SECRET_KEY: SecretStr = Field(..., description="JWT secret key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # Password Policy
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGITS: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # React development server
        "http://localhost:8000",  # FastAPI development server
    ]
    
    # Database
    SQLITE_URL: str = "sqlite+aiosqlite:///./app.db"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False
    
    # Redis Cache
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: Optional[SecretStr] = None
    REDIS_SSL: bool = False
    
    # Qdrant Cloud
    QDRANT_URL: HttpUrl
    QDRANT_API_KEY: SecretStr
    COLLECTION_NAME: str = "documents"
    VECTOR_SIZE: int = 1536  # OpenAI embedding size
    VECTOR_DISTANCE: str = "Cosine"
    VECTOR_ON_DISK: bool = True
    
    # OpenAI
    OPENAI_API_KEY: SecretStr
    OPENAI_ORG_ID: Optional[str] = None
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    COMPLETION_MODEL: str = "gpt-4-0125-preview"
    MAX_TOKENS: int = 500
    TEMPERATURE: float = 0.7
    
    # PDF Processing
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    SUPPORTED_FILE_TYPES: list[str] = ["application/pdf"]
    PROCESSING_TIMEOUT: int = 300  # seconds
    
    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = 30  # seconds
    WS_CLOSE_TIMEOUT: int = 10  # seconds
    
    # Monitoring
    LOG_LEVEL: str = "INFO"
    METRICS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    TRACE_ENABLED: bool = True
    HEALTH_CHECK_INTERVAL: int = 30  # seconds
    
    # Cache
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1 hour
    CACHE_MAX_SIZE: int = 1000  # items
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 3600  # 1 hour
    
    # API Key Management
    API_KEY_ROTATION_DAYS: int = 90
    API_KEY_LENGTH: int = 32
    
    # Backup
    BACKUP_ENABLED: bool = True
    BACKUP_INTERVAL_HOURS: int = 24
    BACKUP_RETENTION_DAYS: int = 30
    BACKUP_PATH: str = "./backups"


# Create settings instance
settings = Settings()


# Example .env file template
ENV_TEMPLATE = """
# Application
DEBUG=false
SECRET_KEY=your-secret-key-here

# Security
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
SQLITE_URL=sqlite+aiosqlite:///./app.db

# Redis Cache
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=optional-redis-password

# Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.cloud
QDRANT_API_KEY=your-qdrant-api-key

# OpenAI
OPENAI_API_KEY=your-openai-api-key
OPENAI_ORG_ID=optional-org-id

# Monitoring
LOG_LEVEL=INFO
METRICS_ENABLED=true
TRACE_ENABLED=true

# Backup
BACKUP_ENABLED=true
BACKUP_PATH=/path/to/backups
""" 