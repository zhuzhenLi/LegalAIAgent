import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz
from .database import Base

# 添加任务类型枚举
class TaskType(str, enum.Enum):
    TASK1 = "TASK1"
    TASK2 = "TASK2"
    TASK3 = "TASK3"
    TASK4 = "TASK4"
    TASK5 = "TASK5"

# 文档状态枚举
class DocumentStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# 文档和会话的多对多关系表
document_session = Table(
    "document_sessions",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("document_id", Integer, ForeignKey("documents.id", ondelete="CASCADE")),
    Column("session_id", Integer, ForeignKey("sessions.id", ondelete="CASCADE")),
    Column("created_at", DateTime(timezone=True), default=lambda: datetime.now(pytz.utc))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), onupdate=lambda: datetime.now(pytz.utc))
    
    # 关系
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), onupdate=lambda: datetime.now(pytz.utc))
    
    # 关系
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="session")
    
    # 多对多关系（可选）
    # all_documents = relationship("Document", secondary=document_session, back_populates="sessions")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    sender = Column(String(50), nullable=False)  # 'user' 或 'ai'
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.utc))
    
    # 关系
    session = relationship("Session", back_populates="messages")

class Document(Base):
    """文档模型，用于存储上传的PDF文件信息"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    text_content = Column(Text, nullable=True)
    task_type = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False)
    result = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), onupdate=lambda: datetime.now(pytz.utc))
    
    # 关系
    user = relationship("User", back_populates="documents")
    session = relationship("Session", back_populates="documents")
    
    # 多对多关系（可选）
    # sessions = relationship("Session", secondary=document_session, back_populates="all_documents")

class Result(Base):
    """结果模型，用于存储AI处理结果"""
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    content = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联文档
    document = relationship("Document", back_populates="results")