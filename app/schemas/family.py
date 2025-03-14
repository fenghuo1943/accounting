from pydantic import Field, EmailStr
from typing import List, Optional
from uuid import UUID
from .base import BaseSchema
from .user import UserRead

class FamilyCreate(BaseSchema):
    name: str

class FamilyRead(BaseSchema):
    id: UUID
    name: str

class FamilyUpdate(BaseSchema):
    name: Optional[str] = None

# 家庭包含成员的响应模型
class FamilyWithMembers(FamilyRead):
    members: List["UserRead"] = []