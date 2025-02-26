from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    DATABASE_URL: str = "sqlite:///./legal_docs.db"
    
    class Config:
        env_file = ".env"

settings = Settings()