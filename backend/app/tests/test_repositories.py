import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.db.base import Base
from app.db.models import User, Document, Session, Message
from app.db.repositories.document_repository import DocumentRepository

# 使用内存数据库进行测试
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    """创建测试数据库会话"""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)

@pytest.fixture
def test_user(db_session):
    """创建测试用户"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_session(db_session, test_user):
    """创建测试会话"""
    session = Session(
        title="测试会话",
        user_id=test_user.id
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    return session

def test_document_repository_create(db_session, test_user, test_session):
    """测试文档仓库的创建功能"""
    repo = DocumentRepository(db_session)
    
    document_data = {
        "filename": "test_document.pdf",
        "file_path": "/uploads/test_document.pdf",
        "file_type": ".pdf",
        "text_content": "这是一个测试文档的内容",
        "task_type": "TASK1",
        "status": "uploaded",
        "user_id": test_user.id,
        "session_id": test_session.id
    }
    
    document = repo.create(document_data)
    
    assert document.id is not None
    assert document.filename == "test_document.pdf"
    assert document.status == "uploaded"
    assert document.user_id == test_user.id
    assert document.session_id == test_session.id

def test_document_repository_get_by_id(db_session, test_user, test_session):
    """测试文档仓库的按ID获取功能"""
    repo = DocumentRepository(db_session)
    
    # 创建文档
    document_data = {
        "filename": "test_document.pdf",
        "file_path": "/uploads/test_document.pdf",
        "file_type": ".pdf",
        "text_content": "这是一个测试文档的内容",
        "task_type": "TASK1",
        "status": "uploaded",
        "user_id": test_user.id,
        "session_id": test_session.id
    }
    
    created_document = repo.create(document_data)
    
    # 获取文档
    document = repo.get_by_id(created_document.id)
    
    assert document is not None
    assert document.id == created_document.id
    assert document.filename == "test_document.pdf"

def test_document_repository_update(db_session, test_user, test_session):
    """测试文档仓库的更新功能"""
    repo = DocumentRepository(db_session)
    
    # 创建文档
    document_data = {
        "filename": "test_document.pdf",
        "file_path": "/uploads/test_document.pdf",
        "file_type": ".pdf",
        "text_content": "这是一个测试文档的内容",
        "task_type": "TASK1",
        "status": "uploaded",
        "user_id": test_user.id,
        "session_id": test_session.id
    }
    
    document = repo.create(document_data)
    
    # 更新文档
    update_data = {
        "status": "processing",
        "result": "处理中..."
    }
    
    updated_document = repo.update(document.id, update_data)
    
    assert updated_document is not None
    assert updated_document.status == "processing"
    assert updated_document.result == "处理中..."

def test_document_repository_delete(db_session, test_user, test_session):
    """测试文档仓库的删除功能"""
    repo = DocumentRepository(db_session)
    
    # 创建文档
    document_data = {
        "filename": "test_document.pdf",
        "file_path": "/uploads/test_document.pdf",
        "file_type": ".pdf",
        "text_content": "这是一个测试文档的内容",
        "task_type": "TASK1",
        "status": "uploaded",
        "user_id": test_user.id,
        "session_id": test_session.id
    }
    
    document = repo.create(document_data)
    
    # 删除文档
    result = repo.delete(document.id)
    
    assert result is True
    
    # 确认文档已删除
    deleted_document = repo.get_by_id(document.id)
    assert deleted_document is None 