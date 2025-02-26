from sqlalchemy.orm import Session
from ..models.document import Document
from typing import List, Optional

class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, document_data: dict) -> Document:
        """创建新文档"""
        db_document = Document(**document_data)
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        return db_document
    
    def get_by_id(self, document_id: int) -> Optional[Document]:
        """通过ID获取文档"""
        return self.db.query(Document).filter(Document.id == document_id).first()
    
    def get_by_user(self, user_id: int) -> List[Document]:
        """获取用户的所有文档"""
        return self.db.query(Document).filter(Document.user_id == user_id).all()
    
    def update(self, document_id: int, update_data: dict) -> Optional[Document]:
        """更新文档"""
        document = self.get_by_id(document_id)
        if not document:
            return None
        
        for key, value in update_data.items():
            setattr(document, key, value)
        
        self.db.commit()
        self.db.refresh(document)
        return document
    
    def delete(self, document_id: int) -> bool:
        """删除文档"""
        document = self.get_by_id(document_id)
        if not document:
            return False
        
        self.db.delete(document)
        self.db.commit()
        return True 