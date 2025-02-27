from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User

# 创建OAuth2密码承载令牌
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 获取当前用户
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # 这里应该验证令牌并获取用户
    # 简化起见，我们直接返回一个模拟用户
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        # 如果没有admin用户，创建一个
        user = User(
            username="admin",
            email="admin@example.com",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user 