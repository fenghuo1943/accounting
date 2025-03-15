# 启动 FastAPI
#uvicorn main:app --reload
# 启动 Celery Worker
#celery -A app.core.celery worker --loglevel=info
from fastapi import FastAPI
from app.core.config import settings
from app.api import transaction, user, account,family
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="智能记账系统 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)
# 加载路由
app.include_router(transaction.router, prefix="/api/v1")
app.include_router(account.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(family.router, prefix="/api/v1")
#app.include_router(auth.router, prefix="/api/v1/auth")

@app.get("/")
def read_root():
    return {"message": "欢迎使用智能记账系统 API"}