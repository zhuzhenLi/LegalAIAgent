from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
import os
import uuid
from app.services.pdf_service import extract_text_from_pdf

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

# 存储上传的文件信息
uploaded_files = {}

@router.post("/upload")
async def upload_document(
    files: List[UploadFile] = File(...),
    task_type: str = Form(...)
):
    """
    上传文档
    
    Args:
        files: 上传的文件列表
        task_type: 任务类型，如 "TASK1"
        
    Returns:
        dict: 包含上传结果的字典
    """
    # 验证任务类型
    valid_task_types = ["TASK1", "TASK2", "TASK3", "TASK4", "TASK5"]
    
    if task_type not in valid_task_types:
        print(f"Warning: Unknown task_type '{task_type}'")
    
    # 处理上传的文件
    uploaded_documents = []
    
    for file in files:
        try:
            # 创建上传目录
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)
            
            # 生成唯一文件名
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(upload_dir, unique_filename)
            
            # 保存文件
            with open(file_path, "wb") as f:
                f.write(await file.read())
            
            # 提取文本
            text = extract_text_from_pdf(file_path)
            text_length = len(text)
            
            # 生成文件ID
            file_id = len(uploaded_files) + 1
            
            # 存储文件信息
            uploaded_files[file_id] = {
                "id": file_id,
                "filename": file.filename,
                "file_path": file_path,
                "task_type": task_type,
                "text": text,
                "status": "uploaded"
            }
            
            # 添加到上传文档列表
            uploaded_documents.append({
                "file_id": file_id,
                "filename": file.filename,
                "task_type": task_type,
                "text_length": text_length,
                "status": "uploaded"
            })
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"处理文件 {file.filename} 时出错: {str(e)}")
    
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