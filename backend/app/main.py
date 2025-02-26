from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from .database import engine
from .models import Base
from .routers import documents, ai
import os

# 创建上传目录
os.makedirs("uploads", exist_ok=True)

# 创建应用
app = FastAPI(title="Legal AI API")

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 配置跨域资源共享(CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加CSP中间件
@app.middleware("http")
async def add_csp_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-eval'; connect-src 'self' http://localhost:8000; style-src 'self' 'unsafe-inline';"
    return response

# 注册路由
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Legal AI API"}

@app.post("/upload")
async def upload_redirect(request: Request):
    """重定向到/documents/upload"""
    return RedirectResponse(url="/documents/upload")

@app.post("/process")
async def process_redirect(request: Request):
    """重定向到/ai/process"""
    return RedirectResponse(url="/ai/process")

@app.get("/result/{file_id}")
async def result_redirect(file_id: int):
    """重定向到/ai/result/{file_id}"""
    return RedirectResponse(url=f"/ai/result/{file_id}")