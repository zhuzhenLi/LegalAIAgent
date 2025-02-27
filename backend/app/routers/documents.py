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
    task_type: str = Form(default="default")
):
    """
    上传文档
    
    Args:
        files: 上传的文件列表
        task_type: 任务类型
        
    Returns:
        dict: 包含上传结果的字典
    """
    print(f"Received upload request with {len(files)} files and task_type: {task_type}")
    
    # 创建上传目录
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    uploaded_documents = []
    
    for file in files:
        print(f"Processing file: {file.filename}")
        # 生成唯一文件ID
        file_id = len(uploaded_files) + 1
        
        # 保存文件
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        print(f"File saved to: {file_path}")
        
        # 提取文本
        text = extract_text_from_pdf(file_path)
        text_length = len(text)
        
        print(f"Extracted text length: {text_length}")
        
        # 存储文档信息
        uploaded_files[file_id] = {
            "id": file_id,
            "filename": file.filename,
            "file_path": file_path,
            "task_type": task_type,
            "text": text,
            "text_length": text_length,
            "status": "uploaded",
            "upload_time": datetime.now().isoformat()
        }
        
        uploaded_documents.append({
            "id": file_id,
            "filename": file.filename,
            "task_type": task_type,
            "text_length": text_length,
            "status": "uploaded"
        })
    
    response_data = {
        "message": f"成功上传 {len(uploaded_documents)} 个文件",
        "documents": uploaded_documents
    }
    print(f"Upload response: {response_data}")
    return response_data

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