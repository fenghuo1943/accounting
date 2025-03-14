from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate, UserUpdate, UserRead
import uuid

class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        existing_user = db.query(User).filter(
            (User.username == user_data.username) | (User.email == user_data.email)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists"
            )

        # 创建用户并哈希密码
        user = User(
            id=str(uuid.uuid4()),  # 生成 UUID
            username=user_data.username,
            email=user_data.email
        )
        user.set_password(user_data.password)  # 哈希密码
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # 更新用户名和邮箱
        if user_data.username:
            user.username = user_data.username
        if user_data.email:
            user.email = user_data.email

        # 更新密码（如果提供了新密码）
        if user_data.password:
            user.set_password(user_data.password)  # 哈希新密码

        db.commit()
        db.refresh(user)
        return user
    @staticmethod
    def get_user_by_id(db: Session, user_id: str):
        try:
            user_uuid = uuid.UUID(user_id)  # 将字符串转换为 UUID
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}