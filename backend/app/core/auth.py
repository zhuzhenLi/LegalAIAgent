from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 这是一个简化版本，实际应用中应该使用JWT或其他认证机制
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # 在实际应用中，你应该验证token并获取用户ID
    # 这里简化为直接获取用户ID=1的用户
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user 