from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import BaseModel
import uuid

class Family(BaseModel):
    __tablename__ = "families"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    name = Column(String(50), nullable=False)

    # 家庭与用户的关系（一对多）
    users = relationship("User", back_populates="family")  