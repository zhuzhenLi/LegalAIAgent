from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取数据库连接URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ligege:923180@localhost/legal_ai")

# 创建引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 依赖项，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建所有表
def create_tables():
    # 导入所有模型以确保它们被注册到Base元数据
    # 注意：这里的导入应该放在函数内部，避免循环导入
    from .db.models import User, Session, Message, Document
    Base.metadata.create_all(bind=engine)