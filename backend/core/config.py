from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings."""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str
    label_studio_api_key: str
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str