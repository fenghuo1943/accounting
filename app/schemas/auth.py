#认证相关的模型
from pydantic import BaseModel

class Token(BaseModel):
    """
    JWT 令牌模型
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    JWT 令牌数据模型
    """
    user_id: str | None = None