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


settings = Settings()
