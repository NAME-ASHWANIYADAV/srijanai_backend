from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "SrijanAI Creative Suite"
    API_V1_STR: str = "/api/v1"

    # MongoDB
    MONGO_URI: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Email
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # CORS
    BACKEND_CORS_ORIGINS: list[str] | str = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
