from functools import lru_cache
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "sqlite:///./harvestmap.db"
    secret_key: str
    environment: str = "development"
    access_token_minutes: int = 120
    ai_api_key: str = ""
    ai_base_url: str = "https://api.openai.com/v1"
    ai_model: str = "gpt-4o-mini"
    allowed_hosts: str = "localhost,127.0.0.1,testserver"
    secure_cookies: bool = False

    @model_validator(mode="after")
    def secure_secret(self):
        if len(self.secret_key) < 32 or self.secret_key.startswith("REPLACE_"):
            raise ValueError("SECRET_KEY must be a random string of at least 32 characters; run scripts/configure.py")
        if self.environment == "production" and not self.secure_cookies:
            raise ValueError("SECURE_COOKIES=true is required in production")
        return self


@lru_cache
def get_settings():
    return Settings()
