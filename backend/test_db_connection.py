import sys
from pathlib import Path
import logging

# 添加 backend 目录到 Python 路径
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from app.database import engine
from sqlalchemy import text
from sqlalchemy.orm import Session

# 确保导入所有模型
from app.db.models import User, Session as ChatSession, Message, Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """测试数据库连接并查询用户信息"""
    try:
        # 连接数据库
        with Session(engine) as db:
            # 测试连接
            result = db.execute(text("SELECT current_database(), current_user")).fetchone()
            logger.info(f"数据库连接成功! 当前数据库: {result[0]}, 当前用户: {result[1]}")
            
            # 查询表信息
            tables = db.execute(text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            )).fetchall()
            
            logger.info("数据库中的表:")
            for table in tables:
                logger.info(f"  - {table[0]}")
            
            # 查询用户信息
            users = db.query(User).all()
            
            if users:
                logger.info(f"找到 {len(users)} 个用户:")
                for user in users:
                    logger.info(f"  - ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}")
                    
                    # 查询用户的会话
                    sessions = db.query(ChatSession).filter(ChatSession.user_id == user.id).all()
                    
                    if sessions:
                        logger.info(f"    用户 {user.username} 的会话:")
                        for session in sessions:
                            logger.info(f"      - ID: {session.id}, 标题: {session.title}")
                            
                            # 查询会话的消息
                            messages = db.query(Message).filter(Message.session_id == session.id).all()
                            
                            if messages:
                                logger.info(f"        会话 {session.title} 的消息:")
                                for message in messages:
                                    logger.info(f"          - ID: {message.id}, 发送者: {message.sender}, 内容: {message.content[:30]}...")
            else:
                logger.warning("没有找到任何用户，请先运行 init_user.py 创建基础用户")
            
            # 查询文档信息
            documents = db.query(Document).all()
            
            if documents:
                logger.info(f"找到 {len(documents)} 个文档:")
                for doc in documents:
                    logger.info(f"  - ID: {doc.id}, 文件名: {doc.filename}, 状态: {doc.status}")
            else:
                logger.info("没有找到任何文档")
                
            return True
    except Exception as e:
        logger.error(f"数据库连接或查询失败: {str(e)}")
        return False

if __name__ == "__main__":
    if test_connection():
        logger.info("数据库连接测试成功!")
    else:
        logger.error("数据库连接测试失败!") 