# backend/app/core/config.py

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str = "sqlite:///./emailproai.db"
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"
    
    # Gmail OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    
    # SMTP fallback
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    
    # Cashfree Payment Gateway
    CASHFREE_APP_ID: str = ""
    CASHFREE_SECRET_KEY: str = ""

    # Add these new configuration fields
    MICROSOFT_CLIENT_ID: str = ""
    MICROSOFT_CLIENT_SECRET: str = ""
    FCM_SERVER_KEY: str = ""
    SLACK_WEBHOOK_URL: str = ""

    # CRM Integration
    SALESFORCE_CLIENT_ID: str = ""
    SALESFORCE_CLIENT_SECRET: str = ""
    HUBSPOT_API_KEY: str = ""

    # White Label
    ENABLE_WHITE_LABEL: bool = False
    DEFAULT_BRAND_NAME: str = "EmailProAI"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()
