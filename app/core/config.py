from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Pearl API"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"


settings = Settings()