import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    """应用配置"""
    # 应用名称
    APP_NAME: str = "PDF处理系统"
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # OpenAI API配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # 跨域配置
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"

# 创建设置实例
settings = Settings()