from ..db.repositories.document_repository import DocumentRepository
from ..db.session import get_db_session
from ..services.pdf_service import extract_text_from_pdf
import os
from typing import List, Dict, Any
from fastapi import UploadFile
from datetime import datetime

class DocumentService:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository
        
    async def upload_document(self, file: UploadFile, user_id: int, session_id: int = None):
        # 1. 保存文件到磁盘
        file_path = f"uploads/{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 2. 获取文件类型
        file_type = file.content_type
        
        # 3. 提取文本内容（如果是PDF）
        text_content = None
        if file_type == "application/pdf":
            text_content = extract_text_from_pdf(file_path)
        
        # 4. 创建文档记录
        document = {
            "filename": file.filename,
            "file_path": file_path,
            "file_type": file_type,
            "text_content": text_content,
            "status": "uploaded",
            "user_id": user_id,
            "session_id": session_id
        }
        
        # 5. 保存到数据库
        document_id = await self.document_repository.create(document)
        
        return {
            "id": document_id,
            "filename": file.filename,
            "status": "uploaded",
            "created_at": datetime.now().isoformat()
        } 