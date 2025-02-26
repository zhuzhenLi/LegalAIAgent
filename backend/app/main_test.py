from fastapi import FastAPI
from app.models import Base
from app.database import engine

# 创建所有表
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "测试成功"} 