from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    ADMIN_PASSWORD: str = "george2024"
    DATABASE_URL: str = "sqlite:///./geek_site.db"
    SECRET_KEY: str = "geek-site-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache()
def get_settings():
    return Settings()
