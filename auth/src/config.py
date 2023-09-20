import os
import logging

from functools import lru_cache

from pydantic import AnyUrl

log = logging.getLogger("uvicorn")


class Settings:
    MONGODB_URL: AnyUrl = os.environ.get("MONGODB_URL")
    ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS").split(" ")
    ALGORITHM: str = os.environ.get("ALGORITHM")
    JWT_KEY: str = os.environ.get("SECRET_KEY")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME")

    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()


settings = get_settings()
