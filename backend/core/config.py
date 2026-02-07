from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # Pydantic will automatically look for a GOOGLE_API_KEY env var
    # If it's missing, it will raise an error on startup
    google_api_key: str
    
    # App Settings
    app_name: str = "Content Alchemist API"
    debug: bool = False

    # This tells Pydantic to read from your .env file
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # Ignores extra variables in .env not defined here
    )

@lru_cache
def get_settings():
    """
    Uses lru_cache to ensure we only load the .env file once,
    even if we call get_settings() multiple times.
    """
    return Settings()

settings = get_settings()
