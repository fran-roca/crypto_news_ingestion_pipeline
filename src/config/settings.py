from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    NEWS_API_KEY: str
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str
    LOG_TO_FILE: bool = True  # Defaults to True if not provided in .env

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()