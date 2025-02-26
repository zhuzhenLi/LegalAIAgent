from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
import uuid

class Document(Base):
    """
    文档模型
    用于存储上传的PDF文件信息
    """
    __tablename__ = "documents"
    
    # 使用UUID作为主键
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # 文件原始名称
    filename = Column(String, nullable=False)
    # 文件存储路径
    file_path = Column(String, nullable=False)
    # 上传时间
    upload_time = Column(DateTime, default=datetime.utcnow)
    # 文档状态（如：pending, processed等）
    status = Column(String, default="pending")
    # 关联的案件ID
    case_id = Column(String, ForeignKey("cases.id"))
    
    # 与Case模型的关系
    case = relationship("Case", back_populates="documents")

class Case(Base):
    """
    案件模型
    用于存储案件信息
    """
    __tablename__ = "cases"
    
    # 使用UUID作为主键
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # 案件标题
    title = Column(String, nullable=False)
    # 任务类型（如：诉讼书、应诉书）
    task_type = Column(String, nullable=False)
    # 创建时间
    created_at = Column(DateTime, default=datetime.utcnow)
    # AI分析结果
    result = Column(String, nullable=True)
    
    # 与Document模型的关系
    documents = relationship("Document", back_populates="case")