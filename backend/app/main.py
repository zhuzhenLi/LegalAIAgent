from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
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
async def root():
    return {"message": "PDF处理系统API"}

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