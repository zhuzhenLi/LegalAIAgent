import sys
import os
from pathlib import Path

# 添加 backend 目录到 Python 路径
backend_dir = Path(__file__).parent.parent.parent
sys.path.append(str(backend_dir))

from app.database import engine, Base
from app.db.models import User, Session, Message, Document
import logging

logger = logging.getLogger(__name__)

def init_db():
    """
    初始化数据库，创建所有表
    """
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表已创建")

    # 这里可以添加初始数据
    # 例如创建管理员用户等

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
    logger.info("数据库初始化完成")