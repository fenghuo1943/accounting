#账户的创建和读取模型
from pydantic import Field
from uuid import UUID
from .base import BaseSchema

class AccountCreate(BaseSchema):
    name: str = Field(..., description="账户名称")
    type: str = Field(..., description="账户类型")
    balance: float = Field(default=0.0)
    allow_negative: bool = Field(True, description="是否允许负余额")
    user_id: str

class AccountRead(BaseSchema):
    id: UUID
    name: str
    type: str
    balance: float
    allow_negative: bool
    user_id: UUID

class AccountUpdate(BaseSchema):
    name: str | None = None
    balance: float | None = None
    allow_negative: bool | None = None