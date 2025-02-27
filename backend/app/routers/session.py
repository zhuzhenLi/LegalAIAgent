from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User, Session as ChatSession, Message
from app.auth import get_current_user

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.get("/", response_model=List[dict])
def get_sessions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取当前用户的所有会话"""
    sessions = db.query(ChatSession).filter(ChatSession.user_id == current_user.id).all()
    return [{"id": s.id, "title": s.title, "created_at": s.created_at} for s in sessions]

@router.post("/", response_model=dict)
def create_session(title: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """创建新会话"""
    session = ChatSession(title=title, user_id=current_user.id)
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # 创建欢迎消息
    welcome_message = Message(
        content="Hello! How can I help you with legal documents today?",
        sender="ai",
        session_id=session.id
    )
    db.add(welcome_message)
    db.commit()
    
    return {"id": session.id, "title": session.title, "created_at": session.created_at}

@router.get("/{session_id}", response_model=dict)
def get_session(session_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取特定会话的详情"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"id": session.id, "title": session.title, "created_at": session.created_at} 