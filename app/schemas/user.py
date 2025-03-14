#用户的创建和读取模型
from pydantic import Field, EmailStr
from uuid import UUID
from .base import BaseSchema
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseSchema):
    username: str = Field(..., description="用户名")
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., description="用户密码")

class UserRead(BaseSchema):
    id: UUID
    username: str
    email: EmailStr
class UserUpdate(BaseSchema):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

# 用户登录请求模型
class UserLogin(BaseModel):
    username: str
    password: str