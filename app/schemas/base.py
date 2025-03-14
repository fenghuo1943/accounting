from pydantic import BaseModel

class BaseSchema(BaseModel):
    """
    基础模型，包含通用字段
    """
    class Config:
        from_attributes = True  # 允许从 ORM 模型实例化