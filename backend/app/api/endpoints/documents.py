from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...services.document_service import DocumentService
from ...core.auth import get_current_user
from ...db.models.user import User

router = APIRouter()
document_service = DocumentService()

@router.post("/upload")
async def upload_document(
    files: List[UploadFile] = File(...),
    task_type: str = Form(default="default"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传文档"""
    uploaded_documents = []
    
    for file in files:
        content = await file.read()
        document = document_service.upload_document(
            file_data=content,
            filename=file.filename,
            user_id=current_user.id,
            task_type=task_type
        )
        uploaded_documents.append(document)
    
    return {
        "message": f"成功上传 {len(uploaded_documents)} 个文件",
        "documents": uploaded_documents
    } 