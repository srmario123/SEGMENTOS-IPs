from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ISP IP Segment Manager"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 720
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/ip_segments"
    cors_origins: str = "http://localhost:5173"
    global_snmp_community: str = "public"
    scheduler_enabled: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
