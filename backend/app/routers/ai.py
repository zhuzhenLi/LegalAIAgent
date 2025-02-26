from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.routers.documents import uploaded_files

router = APIRouter(
    prefix="/ai",
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

@router.post("/process")
async def process_document_route(request: ProcessRequest):
    """
    处理文档
    
    Args:
        request: 包含文档ID和任务类型的请求
        
    Returns:
        dict: 处理结果
    """
    file_id = request.file_id
    task_type = request.task_type
    
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail=f"Document with ID {file_id} not found")
    
    document = uploaded_files[file_id]
    
    # 更新文档状态
    document["status"] = "processing"
    
    try:
        # 获取文本内容
        text = document["text"]
        
        # 根据任务类型选择不同的行
        lines = text.split('\n')
        
        result_content = ""
        if task_type == "TASK1" and len(lines) > 0:
            result_content = f"TASK1 结果: {lines[0]}"
        elif task_type == "TASK2" and len(lines) > 1:
            result_content = f"TASK2 结果: {lines[1]}"
        elif task_type == "TASK3" and len(lines) > 2:
            result_content = f"TASK3 结果: {lines[2]}"
        elif task_type == "TASK4" and len(lines) > 3:
            result_content = f"TASK4 结果: {lines[3]}"
        elif task_type == "TASK5" and len(lines) > 4:
            result_content = f"TASK5 结果: {lines[4]}"
        else:
            result_content = f"{task_type} 结果: 无法获取指定行，PDF内容不足"
        
        # 存储处理结果
        document["result"] = result_content
        document["status"] = "completed"
        
        return {"status": "success", "message": "Document processed successfully"}
        
    except Exception as e:
        document["status"] = "failed"
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