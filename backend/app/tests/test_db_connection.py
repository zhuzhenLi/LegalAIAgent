import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.db.session import engine, get_db_session
from app.db.base import Base
from app.db.models import User, Document, Session, Message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """测试数据库连接"""
    try:
        # 尝试连接数据库
        connection = engine.connect()
        logger.info("数据库连接成功!")
        connection.close()
        return True
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        return False

def test_create_tables():
    """测试创建所有表"""
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("所有表创建成功!")
        return True
    except Exception as e:
        logger.error(f"创建表失败: {str(e)}")
        return False

if __name__ == "__main__":
    if test_connection():
        test_create_tables() 