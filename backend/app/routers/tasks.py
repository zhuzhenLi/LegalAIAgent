from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional

router = APIRouter()

# 存储任务信息
tasks = {}

@router.post("/process")
async def process_task(task_data: Dict[str, Any]):
    """
    处理任务
    
    Args:
        task_data: 任务数据
        
    Returns:
        dict: 包含任务ID的字典
    """
    task_id = len(tasks) + 1
    
    tasks[task_id] = {
        "id": task_id,
        "status": "processing",
        "data": task_data,
        "result": None
    }
    
    return {"task_id": task_id}

@router.get("/{task_id}")
async def get_task(task_id: int):
    """
    获取任务状态
    
    Args:
        task_id: 任务ID
        
    Returns:
        dict: 包含任务状态的字典
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    
    # 模拟任务完成
    if tasks[task_id]["status"] == "processing":
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["result"] = {
            "current_output": "这是一个示例输出。实际输出将基于您的任务类型和输入数据。"
        }
    
    return tasks[task_id] 