import sys
from pathlib import Path

# 添加 backend 目录到 Python 路径
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from app.database import Base, engine
from app.db.models import User, Session, Message, Document

def check_metadata():
    """检查 SQLAlchemy 元数据"""
    print("检查 SQLAlchemy 元数据...")
    print(f"元数据中的表: {Base.metadata.tables.keys()}")
    
    # 确保所有模型都被导入
    print("\n已导入的模型:")
    models = [User, Session, Message, Document]
    for model in models:
        print(f"  {model.__name__}: {model.__tablename__}")
    
    # 检查表是否存在于数据库中
    print("\n数据库中的表:")
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    for table in tables:
        print(f"  {table}")
    
    # 创建表
    print("\n尝试创建表...")
    Base.metadata.create_all(engine)
    print("表创建完成")
    
    # 再次检查数据库中的表
    print("\n创建后数据库中的表:")
    tables = inspector.get_table_names()
    for table in tables:
        print(f"  {table}")

if __name__ == "__main__":
    check_metadata() 