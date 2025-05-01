import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    OPENAI_API_KEY: str
    STRIPE_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
