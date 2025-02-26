import sys
from pathlib import Path
import logging

# 添加 backend 目录到 Python 路径
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from app.database import engine, Base
from sqlalchemy import text

# 确保导入所有模型
from app.db.models import User, Session, Message, Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_db():
    """重置数据库，删除所有表并重新创建"""
    # 删除所有表
    logger.info("删除所有表...")
    Base.metadata.drop_all(bind=engine)
    logger.info("所有表已删除")
    
    # 创建所有表
    logger.info("创建所有表...")
    Base.metadata.create_all(bind=engine)
    logger.info("所有表已创建")
    
    # 验证表是否创建成功
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    logger.info(f"数据库中的表: {tables}")
    
    # 检查是否所有表都创建成功
    expected_tables = {"users", "documents", "sessions", "messages"}
    if all(table in tables for table in expected_tables):
        logger.info("所有表都创建成功!")
    else:
        missing_tables = expected_tables - set(tables)
        logger.error(f"缺少以下表: {missing_tables}")

if __name__ == "__main__":
    reset_db() 