import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    admin: str = os.environ.get("username_db", "")
    password: str = os.environ.get("password", "")
    host: str = os.environ.get("host", "")
    port: int = os.environ.get("port", 0)
    database: str = os.environ.get("database", "")


settings_DB = Settings()
