import sys
import os
from pathlib import Path

# 添加 backend 目录到 Python 路径
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from app.database import Base
from app.db.models import User, Session, Message, Document
from sqlalchemy import inspect

def check_models():
    """检查模型映射"""
    models = [User, Session, Message, Document]
    
    for model in models:
        print(f"检查模型: {model.__name__}")
        print(f"  表名: {model.__tablename__}")
        
        mapper = inspect(model)
        print("  列:")
        for column in mapper.columns:
            print(f"    {column.name}: {column.type}")
        
        print("  关系:")
        for relationship in mapper.relationships:
            print(f"    {relationship.key}: {relationship.target}")
        
        print()

if __name__ == "__main__":
    check_models()