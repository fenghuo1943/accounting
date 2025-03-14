#账单模型
from datetime import datetime
from sqlalchemy import Column, Numeric, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import BaseModel
import uuid

class Transaction(BaseModel):
    __tablename__ = "transactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    type = Column(String(20), nullable=False)
    amount = Column(Numeric(16, 2), nullable=False)
    #to_account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    # 关系
    from_account_id = Column(String, ForeignKey("accounts.id"))
    from_account = relationship("Account", back_populates="transactions")
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="transactions")