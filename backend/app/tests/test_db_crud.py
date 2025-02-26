import sys
import os
import logging
from pathlib import Path
from datetime import datetime
import pytz

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.db.session import get_db_session
from app.db.models import User, Document, Session, Message
from app.db.repositories.document_repository import DocumentRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_user():
    """创建测试用户"""
    with get_db_session() as db:
        # 检查用户是否已存在
        existing_user = db.query(User).filter(User.username == "testuser").first()
        if existing_user:
            logger.info(f"测试用户已存在: {existing_user.username}")
            return existing_user
        
        # 创建新用户
        new_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password_here"  # 实际应用中应该使用加密密码
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"创建测试用户成功: {new_user.username}")
        return new_user

def create_test_session(user_id):
    """创建测试会话"""
    with get_db_session() as db:
        # 创建新会话
        new_session = Session(
            title="测试会话",
            user_id=user_id
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        logger.info(f"创建测试会话成功: {new_session.title}")
        return new_session

def create_test_document(user_id, session_id):
    """创建测试文档"""
    with get_db_session() as db:
        # 使用仓库模式创建文档
        repo = DocumentRepository(db)
        document_data = {
            "filename": "test_document.pdf",
            "file_path": "/uploads/test_document.pdf",
            "file_type": ".pdf",
            "text_content": "这是一个测试文档的内容",
            "task_type": "TASK1",
            "status": "uploaded",
            "user_id": user_id,
            "session_id": session_id
        }
        document = repo.create(document_data)
        logger.info(f"创建测试文档成功: {document.filename}")
        return document

def create_test_message(session_id):
    """创建测试消息"""
    with get_db_session() as db:
        # 创建用户消息
        user_message = Message(
            content="这是一个测试问题",
            sender="user",
            session_id=session_id
        )
        db.add(user_message)
        
        # 创建AI回复
        ai_message = Message(
            content="这是AI的测试回复",
            sender="ai",
            session_id=session_id
        )
        db.add(ai_message)
        
        db.commit()
        logger.info("创建测试消息成功")
        return user_message, ai_message

def query_test_data():
    """查询测试数据"""
    with get_db_session() as db:
        # 查询用户
        user = db.query(User).filter(User.username == "testuser").first()
        if user:
            logger.info(f"查询用户成功: {user.username}, {user.email}")
            
            # 查询用户的会话
            sessions = db.query(Session).filter(Session.user_id == user.id).all()
            logger.info(f"用户的会话数量: {len(sessions)}")
            
            for session in sessions:
                logger.info(f"会话: {session.title}, 创建时间: {session.created_at}")
                
                # 查询会话的消息
                messages = db.query(Message).filter(Message.session_id == session.id).all()
                logger.info(f"会话的消息数量: {len(messages)}")
                
                for message in messages:
                    logger.info(f"消息: {message.sender} - {message.content[:30]}...")
                
                # 查询会话的文档
                documents = db.query(Document).filter(Document.session_id == session.id).all()
                logger.info(f"会话的文档数量: {len(documents)}")
                
                for document in documents:
                    logger.info(f"文档: {document.filename}, 状态: {document.status}")
        else:
            logger.error("未找到测试用户")

def run_tests():
    """运行所有测试"""
    # 创建测试数据
    user = create_test_user()
    session = create_test_session(user.id)
    document = create_test_document(user.id, session.id)
    messages = create_test_message(session.id)
    
    # 查询测试数据
    query_test_data()

if __name__ == "__main__":
    run_tests() 