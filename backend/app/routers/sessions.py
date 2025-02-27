from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel

router = APIRouter()

# 定义消息模型
class Message(BaseModel):
    content: str
    sender: str

# 存储会话信息
sessions = {}

@router.post("/{session_id}/messages")
async def create_message(session_id: str, message: Message):
    """
    创建消息
    
    Args:
        session_id: 会话ID
        message: 消息内容
        
    Returns:
        dict: 包含消息ID的字典
    """
    if session_id not in sessions:
        sessions[session_id] = []
    
    message_id = len(sessions[session_id]) + 1
    
    # 存储消息
    sessions[session_id].append({
        "id": message_id,
        "content": message.content,
        "sender": message.sender
    })
    
    # 如果是用户消息，添加AI回复
    if message.sender == "user":
        ai_message_id = len(sessions[session_id]) + 1
        sessions[session_id].append({
            "id": ai_message_id,
            "content": f"这是对 '{message.content}' 的AI回复",
            "sender": "ai"
        })
    
    return {"message_id": message_id}

@router.get("/{session_id}/messages")
async def get_messages(session_id: str):
    """
    获取会话消息
    
    Args:
        session_id: 会话ID
        
    Returns:
        list: 包含会话消息的列表
    """
    if session_id not in sessions:
        return []
    
    return sessions[session_id] 