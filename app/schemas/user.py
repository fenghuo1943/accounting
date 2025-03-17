#用户的创建和读取模型
from pydantic import Field, EmailStr
from uuid import UUID
from .base import BaseSchema
from pydantic import EmailStr, Field

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
class UserLogin(BaseSchema):
    username: str
    password: str

# 用户注册请求模型
class UserRegister(BaseSchema):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8)  # 密码至少 8 位

# 令牌响应模型
class Token(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str

# 令牌数据模型
class TokenData(BaseSchema):
    username: str | None = None