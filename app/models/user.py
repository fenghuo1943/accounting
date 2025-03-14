# models/user.py
from sqlalchemy import Column,Integer, String, Boolean,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from .base import BaseModel
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    __tablename__ = "users"
    
    #id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    #hashed_password = Column(String(100), nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)

    # 关系
    accounts = relationship("Account", back_populates="user")  # 一对多：用户 -> 账户
    family_id = Column(String, ForeignKey("families.id"), nullable=True)
    family = relationship("Family", back_populates="users")

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    # 密码验证方法
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)