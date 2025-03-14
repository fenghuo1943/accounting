from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 项目配置
    PROJECT_NAME: str = "智能记账系统"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # 数据库配置
    DATABASE_URL: str = "postgresql://postgres:wzcx131130@localhost:5432/accounting"

    # JWT 配置
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # Celery 配置
    CELERY_BROKER_URL: str = "redis://172.24.132.246:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://172.24.132.246:6379/1"

    class Config:
        env_file = ".env"  # 从 .env 文件加载环境变量

# 全局配置实例
settings = Settings()