import argparse
import logging
from pathlib import Path
import sys

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.db.session import engine, get_db_session
from app.db.base import Base
from app.db.models import User, Document, Session, Message
from app.db.init_db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """创建所有表"""
    Base.metadata.create_all(bind=engine)
    logger.info("所有表创建成功!")

def drop_tables():
    """删除所有表"""
    Base.metadata.drop_all(bind=engine)
    logger.info("所有表删除成功!")

def reset_database():
    """重置数据库"""
    drop_tables()
    create_tables()
    logger.info("数据库重置成功!")

def create_admin_user(username, email, password):
    """创建管理员用户"""
    with get_db_session() as db:
        # 检查用户是否已存在
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            logger.info(f"用户已存在: {existing_user.username}")
            return
        
        # 创建新用户
        new_user = User(
            username=username,
            email=email,
            hashed_password=password  # 实际应用中应该使用加密密码
        )
        db.add(new_user)
        db.commit()
        logger.info(f"创建用户成功: {username}")

def list_users():
    """列出所有用户"""
    with get_db_session() as db:
        users = db.query(User).all()
        logger.info(f"用户数量: {len(users)}")
        for user in users:
            logger.info(f"用户ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}")

def list_documents():
    """列出所有文档"""
    with get_db_session() as db:
        documents = db.query(Document).all()
        logger.info(f"文档数量: {len(documents)}")
        for doc in documents:
            logger.info(f"文档ID: {doc.id}, 文件名: {doc.filename}, 状态: {doc.status}")

def main():
    parser = argparse.ArgumentParser(description="数据库管理工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 创建表命令
    create_parser = subparsers.add_parser("create", help="创建所有表")
    
    # 删除表命令
    drop_parser = subparsers.add_parser("drop", help="删除所有表")
    
    # 重置数据库命令
    reset_parser = subparsers.add_parser("reset", help="重置数据库")
    
    # 初始化数据库命令
    init_parser = subparsers.add_parser("init", help="初始化数据库")
    
    # 创建管理员用户命令
    admin_parser = subparsers.add_parser("create-admin", help="创建管理员用户")
    admin_parser.add_argument("--username", required=True, help="用户名")
    admin_parser.add_argument("--email", required=True, help="邮箱")
    admin_parser.add_argument("--password", required=True, help="密码")
    
    # 列出用户命令
    list_users_parser = subparsers.add_parser("list-users", help="列出所有用户")
    
    # 列出文档命令
    list_docs_parser = subparsers.add_parser("list-docs", help="列出所有文档")
    
    args = parser.parse_args()
    
    if args.command == "create":
        create_tables()
    elif args.command == "drop":
        drop_tables()
    elif args.command == "reset":
        reset_database()
    elif args.command == "init":
        init_db()
    elif args.command == "create-admin":
        create_admin_user(args.username, args.email, args.password)
    elif args.command == "list-users":
        list_users()
    elif args.command == "list-docs":
        list_documents()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 