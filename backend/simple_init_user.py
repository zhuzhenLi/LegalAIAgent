import sys
from pathlib import Path
import logging
import hashlib

# 添加 backend 目录到 Python 路径
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from app.database import engine, Base
from sqlalchemy import text
from sqlalchemy.orm import Session

# 确保导入所有模型
from app.db.models import User, Session as ChatSession, Message, Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_simple_hash(password):
    """简单的密码哈希方法，仅用于测试"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_user():
    """初始化基础用户"""
    # 连接数据库
    with Session(engine) as db:
        # 检查是否已存在用户
        result = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
        
        if result > 0:
            logger.info("用户已存在，跳过创建")
            return
        
        # 创建基础用户
        username = "admin"
        email = "admin@example.com"
        password = "admin123"  # 在实际应用中应使用更强的密码
        
        # 简单哈希密码
        hashed_password = get_simple_hash(password)
        
        # 创建用户
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_active=True
        )
        
        # 添加到数据库
        db.add(user)
        db.commit()
        
        # 获取用户ID
        user_id = user.id
        
        logger.info(f"基础用户创建成功! ID: {user_id}, 用户名: {username}")
        
        # 创建一个初始会话
        session = ChatSession(
            title="Welcome Session",
            user_id=user_id
        )
        
        db.add(session)
        db.commit()
        
        session_id = session.id
        
        logger.info(f"初始会话创建成功! ID: {session_id}")
        
        # 创建欢迎消息 (英文)
        welcome_message = Message(
            content="Welcome to the Legal AI Assistant! I can help you analyze legal documents and answer legal questions. Please upload a document or ask a question to get started.",
            sender="ai",
            session_id=session_id
        )
        
        db.add(welcome_message)
        db.commit()
        
        logger.info("欢迎消息创建成功!")
        
        return user_id

if __name__ == "__main__":
    try:
        user_id = init_user()
        if user_id:
            logger.info(f"基础用户初始化完成! 用户ID: {user_id}")
            logger.info("登录凭据:")
            logger.info("用户名: admin")
            logger.info("密码: admin123")
        else:
            logger.info("基础用户已存在，无需初始化")
    except Exception as e:
        logger.error(f"初始化用户失败: {str(e)}") 