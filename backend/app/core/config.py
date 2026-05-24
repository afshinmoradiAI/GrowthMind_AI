from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str
    google_places_api_key: str | None = None
    default_model: str = "claude-opus-4-7"
    log_level: str = "INFO"
    max_tokens_per_post: int = 2048
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]
    database_url: str = "sqlite:///./growthmind.db"

    jwt_secret: str = "dev-insecure-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 60 * 24 * 7  # 7 days
    cookie_name: str = "growthmind_session"
    cookie_secure: bool = False  # set True in production (HTTPS only)
    cookie_samesite: str = "lax"


settings = Settings()
