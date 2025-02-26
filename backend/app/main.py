from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import documents, ai

# 创建 FastAPI 应用实例
app = FastAPI(title="PDF处理系统")

# 配置跨域资源共享(CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(documents.router)
app.include_router(ai.router)

@app.get("/")
async def root():
    return {"message": "PDF处理系统API"}