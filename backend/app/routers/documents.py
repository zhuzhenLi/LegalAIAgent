from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
import os
import uuid
from app.services.pdf_service import extract_text_from_pdf
from datetime import datetime

router = APIRouter()

# 存储上传的文件信息
uploaded_files = {}

@router.post("/upload")
async def upload_document(
    files: List[UploadFile] = File(...),
    task_type: str = Form(default="default")  # 使用默认值，而不是允许None
):
    """
    上传文档
    
    Args:
        files: 上传的文件列表
        task_type: 任务类型
        
    Returns:
        dict: 包含上传结果的字典
    """
    # 创建上传目录
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    uploaded_documents = []
    
    for file in files:
        # 生成唯一文件ID
        file_id = len(uploaded_files) + 1
        
        # 保存文件
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # 提取文本
        text = extract_text_from_pdf(file_path)
        text_length = len(text)
        
        # 存储文档信息
        uploaded_files[file_id] = {
            "id": file_id,
            "filename": file.filename,
            "file_path": file_path,
            "task_type": task_type,  # 使用提供的任务类型
            "text": text,
            "text_length": text_length,
            "status": "uploaded",
            "upload_time": datetime.now().isoformat()
        }
        
        uploaded_documents.append({
            "id": file_id,
            "filename": file.filename,
            "task_type": task_type,  # 使用提供的任务类型
            "text_length": text_length,
            "status": "uploaded"
        })
    
    return {
        "message": f"成功上传 {len(uploaded_documents)} 个文件",
        "documents": uploaded_documents
    }

@router.get("/{file_id}")
async def get_document(file_id: int):
    """
    获取文档信息
    
    Args:
        file_id: 文档ID
        
    Returns:
        dict: 包含文档信息的字典
    """
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail=f"Document with ID {file_id} not found")
    
    document = uploaded_files[file_id]
    
    return {
        "id": document["id"],
        "filename": document["filename"],
        "task_type": document["task_type"],
        "status": document["status"]
    }