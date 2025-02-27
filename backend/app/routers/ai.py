from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import logging
import re
from ..routers.documents import uploaded_files

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# 存储任务信息
tasks = {}

# 定义请求模型
class ProcessRequest(BaseModel):
    document_ids: List[int]
    task_type: str = "default"

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
    logger.info(f"Processing text with task type: {task_type}")
    
    if not text:
        return "文档内容为空"
    
    # 提取第一句话
    # 尝试使用正则表达式匹配第一个句号、问号或感叹号结束的句子
    match = re.search(r'([^.!?]+[.!?])', text)
    if match:
        first_sentence = match.group(1).strip()
        result = f"文档的第一句话是：\n\n\"{first_sentence}\""
    else:
        # 如果没有找到句号等标点，则使用第一行
        first_line = text.split('\n')[0].strip()
        if first_line:
            result = f"文档的第一行内容是：\n\n\"{first_line}\""
        else:
            result = "无法提取文档的第一句话"
    
    logger.info(f"Processing result: {result[:100]}...")
    return result

@router.post("/process")
async def process_documents(request_data: Dict[str, Any] = Body(...)):
    """
    处理文档
    
    Args:
        request_data: 包含文档ID列表和任务类型的请求
        
    Returns:
        dict: 包含任务ID的字典
    """
    logger.info(f"Received process request: {request_data}")
    
    # 尝试从请求中提取数据
    document_ids = request_data.get("document_ids", [])
    task_type = request_data.get("task_type", "default")
    
    logger.info(f"Processing documents: {document_ids} with task type: {task_type}")
    
    # 验证文档ID
    for doc_id in document_ids:
        if doc_id not in uploaded_files:
            raise HTTPException(status_code=404, detail=f"Document with ID {doc_id} not found")
    
    # 创建任务
    task_id = len(tasks) + 1
    
    # 处理所有文档的文本
    results = []
    for doc_id in document_ids:
        document = uploaded_files[doc_id]
        text = document.get("text", "")
        
        # 根据任务类型处理文本
        processed_result = process_text_by_task(text, task_type)
        results.append(processed_result)
    
    # 合并所有文档的处理结果
    combined_result = "\n\n".join(results)
    
    # 存储任务信息
    tasks[task_id] = {
        "id": task_id,
        "document_ids": document_ids,
        "task_type": task_type,
        "status": "completed",  # 直接设为完成
        "result": {
            "current_output": combined_result
        }
    }
    
    return {"task_id": task_id}

@router.get("/tasks/{task_id}")
async def get_task(task_id: int):
    """
    获取任务状态
    
    Args:
        task_id: 任务ID
        
    Returns:
        dict: 包含任务状态的字典
    """
    logger.info(f"Getting task status for task ID: {task_id}")
    
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    
    return tasks[task_id]

@router.get("/result/{file_id}")
async def get_result(file_id: int):
    """
    获取处理结果
    
    Args:
        file_id: 文件ID
        
    Returns:
        dict: 包含处理结果的字典
    """
    logger.info(f"Getting result for file ID: {file_id}")
    
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail=f"Document with ID {file_id} not found")
    
    document = uploaded_files[file_id]
    
    # 获取文档文本
    text = document.get("text", "")
    
    # 处理文本（默认任务类型）
    result = process_text_by_task(text, "default")
    
    return {
        "file_id": file_id,
        "result": result
    }