from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent


class RabbitMQSettings(BaseModel):
    host: str = f"localhost"


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    rabbit: RabbitMQSettings = RabbitMQSettings()


settings = Settings()
