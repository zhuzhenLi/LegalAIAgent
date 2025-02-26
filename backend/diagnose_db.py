import sys
from pathlib import Path
import logging
import inspect as py_inspect

# 添加 backend 目录到 Python 路径
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from app.database import engine, Base
from sqlalchemy import inspect, text
import sqlalchemy

# 尝试导入所有模型
try:
    from app.db.models import User, Session, Message, Document
    models_imported = True
except Exception as e:
    logging.error(f"导入模型失败: {str(e)}")
    models_imported = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def diagnose_db():
    """诊断数据库问题"""
    logger.info("开始数据库诊断...")
    
    # 检查 SQLAlchemy 版本
    logger.info(f"SQLAlchemy 版本: {sqlalchemy.__version__}")
    
    # 检查数据库连接
    try:
        with engine.connect() as connection:
            logger.info("数据库连接成功!")
            
            # 获取数据库信息
            result = connection.execute(text("SELECT current_database(), current_user"))
            for row in result:
                logger.info(f"当前数据库: {row[0]}, 当前用户: {row[1]}")
            
            # 列出所有表
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            logger.info(f"数据库中的表: {tables}")
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        return
    
    # 检查模型导入
    if models_imported:
        logger.info("模型导入成功")
        
        # 检查每个模型
        models = [User, Session, Message, Document]
        for model in models:
            logger.info(f"检查模型: {model.__name__}")
            logger.info(f"  表名: {model.__tablename__}")
            logger.info(f"  模型定义位置: {py_inspect.getfile(model)}")
            
            # 检查模型的 Base 类
            logger.info(f"  Base 类: {model.__base__}")
            logger.info(f"  Base 类 id: {id(model.__base__)}")
            logger.info(f"  全局 Base 类 id: {id(Base)}")
            
            # 检查模型的列
            logger.info("  列:")
            for column in model.__table__.columns:
                logger.info(f"    {column.name}: {column.type}")
            
            # 检查模型的关系
            if hasattr(model, "__mapper__") and hasattr(model.__mapper__, "relationships"):
                logger.info("  关系:")
                for name, relationship in model.__mapper__.relationships.items():
                    logger.info(f"    {name}: {relationship.target}")
    else:
        logger.error("模型导入失败")
    
    # 检查元数据
    logger.info(f"元数据中的表: {Base.metadata.tables.keys()}")
    
    # 尝试创建表
    try:
        logger.info("尝试创建表...")
        Base.metadata.create_all(engine)
        logger.info("表创建完成")
        
        # 再次列出所有表
        with engine.connect() as connection:
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            logger.info(f"创建后数据库中的表: {tables}")
    except Exception as e:
        logger.error(f"创建表失败: {str(e)}")

if __name__ == "__main__":
    diagnose_db() 