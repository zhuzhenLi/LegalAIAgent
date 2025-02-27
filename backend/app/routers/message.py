from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from pydantic import BaseModel

from app.database import get_db
from app.models import User, Session as ChatSession, Message
from app.auth import get_current_user

router = APIRouter(prefix="/sessions/{session_id}/messages", tags=["messages"])

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    user_message: Dict
    ai_message: Dict

@router.get("/", response_model=List[Dict])
def get_messages(
    session_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """获取会话中的所有消息"""
    # 验证会话属于当前用户
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()
    
    return [
        {
            "id": msg.id,
            "content": msg.content,
            "sender": msg.sender,
            "created_at": msg.created_at
        } 
        for msg in messages
    ]

@router.post("/", response_model=MessageResponse)
def create_message(
    session_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发送新消息并获取AI回复"""
    # 验证会话属于当前用户
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # 保存用户消息
    user_message = Message(
        content=message.content,
        sender="user",
        session_id=session_id
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    # 这里应该调用AI服务生成回复
    # 简化起见，我们直接创建一个模拟回复
    ai_response = "I understand your question about legal documents. Here's my response..."
    
    # 保存AI回复
    ai_message = Message(
        content=ai_response,
        sender="ai",
        session_id=session_id
    )
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)
    
    return {
        "user_message": {
            "id": user_message.id,
            "content": user_message.content,
            "sender": user_message.sender,
            "created_at": user_message.created_at
        },
        "ai_message": {
            "id": ai_message.id,
            "content": ai_message.content,
            "sender": ai_message.sender,
            "created_at": ai_message.created_at
        }
    } 