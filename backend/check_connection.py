import sys
from pathlib import Path

# 添加 backend 目录到 Python 路径
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from app.database import engine
import logging
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_connection():
    """检查数据库连接"""
    try:
        # 尝试连接数据库
        with engine.connect() as connection:
            logger.info("数据库连接成功!")
            
            # 执行简单查询 - 注意使用 text() 函数
            result = connection.execute(text("SELECT current_database(), current_user"))
            for row in result:
                logger.info(f"当前数据库: {row[0]}, 当前用户: {row[1]}")
            
            # 列出所有表
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            logger.info(f"数据库中的表: {tables}")
            
            return True
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        return False

if __name__ == "__main__":
    check_connection() 