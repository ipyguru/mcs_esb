import os
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent


class RabbitMQSettings(BaseModel):
    host: str = os.getenv("RABBITMQ_HOST", "localhost")


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    rabbit: RabbitMQSettings = RabbitMQSettings()
    sentry_sdk_dsn: str = (
        "https://46ad83fa457e0c02222b6bd9c553be3a@o4506860071092224.ingest.us.sentry.io/4506860074631168"
    )


settings = Settings()
