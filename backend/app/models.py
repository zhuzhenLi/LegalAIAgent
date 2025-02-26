import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

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

class Document(Base):
    """文档模型，用于存储上传的PDF文件信息"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.UPLOADED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联结果
    results = relationship("Result", back_populates="document", cascade="all, delete-orphan")

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