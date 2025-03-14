#账单的创建和读取模型
from datetime import datetime
from pydantic import Field
from uuid import UUID
from .base import BaseSchema

class TransactionCreate(BaseSchema):
    type: str = Field(..., description="账单类型（支出、收入、转账）")
    amount: float = Field(..., description="账单金额")
    from_account_id: str = Field(..., description="来源账户ID")
    #to_account_id: UUID | None = Field(None, description="目标账户ID（仅转账类型需要）")
    user_id: str  # 用户 ID（字符串形式的 UUID）
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="账单时间")

class TransactionRead(BaseSchema):
    id: UUID
    type: str
    amount: float
    timestamp: datetime
    from_account_id: UUID
    #to_account_id: UUID | None
    user_id: UUID

class TransactionUpdate(BaseSchema):
    type: str | None = None
    amount: float | None = None
    from_account_id: UUID | None = None
    timestamp: datetime | None = None