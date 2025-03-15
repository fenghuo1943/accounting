#账户模型
from sqlalchemy import Column, String, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import BaseModel
import uuid

class Account(BaseModel):
    __tablename__ = "accounts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    name = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)
    balance = Column(Numeric(19, 4), nullable=False, default=0)
    allow_negative = Column(Boolean, nullable=False, default=True)
    

    # 关系
    user = relationship("User", back_populates="accounts")  # 多对一：账户 -> 用户
    user_id = Column(String, ForeignKey("users.id"))  # 外键：关联用户
    transactions = relationship("Transaction", back_populates="from_account")  # 一对多：账户 -> 账单