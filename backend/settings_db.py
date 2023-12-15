from pydantic_settings import BaseSettings
import os

username = 'postgres'
password = 'adminpass'
host = "127.0.0.1"
port = 5432
database = 'model_result'



class Settings(BaseSettings):
    username: str = os.environ.get("username_db", "")
    password: str = os.environ.get("password", "")
    DATABASE_URL: str = os.environ.get("host", "")
    port : int = os.environ.get("port", 0)
    database : str = os.environ.get("database", "")
    

settings_a = Settings()
