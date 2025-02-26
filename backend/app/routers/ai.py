from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.routers.documents import uploaded_files
import re
from app.services.pdf_service import extract_text_from_pdf

router = APIRouter(
    tags=["ai"]
)

class ProcessRequest(BaseModel):
    file_id: int
    task_type: str
    
    class Config:
        schema_extra = {
            "example": {
                "file_id": 1,
                "task_type": "TASK1"
            }
        }

# 添加这个函数来处理不同任务类型的文本
def process_text_by_task(text, task_type):
    """
    根据任务类型处理文本
    
    Args:
        text: 要处理的文本
        task_type: 任务类型
        
    Returns:
        str: 处理结果
    """
    # 提取第一句话
    match = re.search(r'([^.!?]+[.!?])', text)
    if match:
        first_sentence = match.group(1).strip()
        result_content = f'文档的第一句话是：\n\n"{first_sentence}"'
    else:
        # 如果没有找到句号等标点，则返回前100个字符
        first_part = text[:100].strip() + "..." if len(text) > 100 else text.strip()
        result_content = f'文档的开头内容是：\n\n"{first_part}"'
    
    return result_content

@router.post("/process")
async def process_document(request: ProcessRequest):
    """
    处理文档
    
    Args:
        request: 包含文件ID和任务类型的请求
        
    Returns:
        dict: 处理结果
    """
    file_id = request.file_id
    task_type = request.task_type
    
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail=f"Document with ID {file_id} not found")
    
    document = uploaded_files[file_id]
    file_path = document["file_path"]
    
    try:
        # 更新文档状态为处理中
        document["status"] = "processing"
        
        # 提取文本
        text = extract_text_from_pdf(file_path)
        
        # 根据任务类型处理文本
        result = process_text_by_task(text, task_type)
        
        # 更新文档状态和结果
        document["status"] = "completed"
        document["result"] = result
        
        return {"status": "success", "message": "Document processed successfully"}
    except Exception as e:
        document["status"] = "failed"
        document["error"] = str(e)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.get("/result/{file_id}")
async def get_result_route(file_id: int):
    """
    获取处理结果
    
    Args:
        file_id: 文档ID
        
    Returns:
        dict: 包含结果的字典
    """
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail=f"Document with ID {file_id} not found")
    
    document = uploaded_files[file_id]
    
    if document["status"] == "processing":
        return {"status": "processing", "message": "Document is still being processed"}
    
    elif document["status"] == "failed":
        return {"status": "failed", "message": "Document processing failed"}
    
    elif document["status"] == "completed" and "result" in document:
        return {
            "status": "completed",
            "content": document["result"],
            "document": {
                "id": document["id"],
                "filename": document["filename"],
                "task_type": document["task_type"]
            }
        }
    
    else:
        if document["status"] == "uploaded":
            return {"status": "uploaded", "message": "Document is uploaded but not yet processed. Please call the /ai/process endpoint first."}
        
        return {"status": "unknown", "message": "Result not found or document status is inconsistent"}