import sys
from pathlib import Path
import logging
import argparse

# 添加 backend 目录到 Python 路径
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

# 尝试导入所需的库
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except ImportError:
    print("错误: 缺少必要的库。请运行以下命令安装:")
    print("pip install passlib bcrypt")
    sys.exit(1)

from app.database import engine, Base
from sqlalchemy import text
from sqlalchemy.orm import Session

# 确保导入所有模型
from app.db.models import User, Session as ChatSession, Message, Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_password_hash(password):
    """生成密码哈希"""
    return pwd_context.hash(password)

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
    with engine.connect() as connection:
        result = connection.execute(text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        ))
        tables = [row[0] for row in result]
        logger.info(f"数据库中的表: {tables}")
    
    # 检查是否所有表都创建成功
    expected_tables = {"users", "documents", "sessions", "messages"}
    if all(table in tables for table in expected_tables):
        logger.info("所有表都创建成功!")
    else:
        missing_tables = expected_tables - set(tables)
        logger.error(f"缺少以下表: {missing_tables}")

def create_admin_user(username="admin", email="admin@example.com", password="admin123"):
    """创建管理员用户"""
    with Session(engine) as db:
        # 检查是否已存在用户
        existing_user = db.query(User).filter(User.username == username).first()
        
        if existing_user:
            logger.info(f"用户 {username} 已存在，跳过创建")
            return existing_user.id
        
        # 哈希密码
        hashed_password = get_password_hash(password)
        
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
        db.refresh(user)
        
        logger.info(f"管理员用户创建成功! ID: {user.id}, 用户名: {username}")
        
        return user.id

def create_welcome_session(user_id):
    """为用户创建欢迎会话"""
    with Session(engine) as db:
        # 创建会话
        session = ChatSession(
            title="Welcome Session",
            user_id=user_id
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        logger.info(f"欢迎会话创建成功! ID: {session.id}")
        
        # 创建欢迎消息 (英文)
        welcome_message = Message(
            content="Welcome to the Legal AI Assistant! I can help you analyze legal documents and answer legal questions. Please upload a document or ask a question to get started.",
            sender="ai",
            session_id=session.id
        )
        
        db.add(welcome_message)
        db.commit()
        
        logger.info("欢迎消息创建成功!")
        
        return session.id

def setup_db(reset=False, username="admin", email="admin@example.com", password="admin123"):
    """设置数据库"""
    try:
        # 如果需要重置数据库
        if reset:
            reset_db()
        
        # 创建管理员用户
        user_id = create_admin_user(username, email, password)
        
        # 创建欢迎会话
        session_id = create_welcome_session(user_id)
        
        logger.info("数据库设置完成!")
        logger.info(f"管理员用户 ID: {user_id}")
        logger.info(f"欢迎会话 ID: {session_id}")
        
        return True
    except Exception as e:
        logger.error(f"数据库设置失败: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="设置数据库")
    parser.add_argument("--reset", action="store_true", help="重置数据库（删除所有表并重新创建）")
    parser.add_argument("--username", default="admin", help="管理员用户名")
    parser.add_argument("--email", default="admin@example.com", help="管理员邮箱")
    parser.add_argument("--password", default="admin123", help="管理员密码")
    
    args = parser.parse_args()
    
    if setup_db(args.reset, args.username, args.email, args.password):
        logger.info("数据库设置成功!")
        logger.info("登录凭据:")
        logger.info(f"用户名: {args.username}")
        logger.info(f"密码: {args.password}")
    else:
        logger.error("数据库设置失败!") 