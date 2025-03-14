from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import Family, User
from ..schemas import FamilyCreate, FamilyRead, FamilyUpdate
from uuid import UUID

class FamilyService:
    @staticmethod
    def create_family(self, db: Session, family_data: FamilyCreate):
        existing_family = db.query(Family).filter(Family.name == family_data.name).first()
        if existing_family:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Family name already exists"
            )
        family = Family(name=family_data.name)
        db.add(family)
        db.commit()
        db.refresh(family)
        return family
    @staticmethod
    def get_family_by_id(db: Session, family_id: str):
        family = db.query(Family).filter(Family.id == family_id).first()
        if not family:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Family not found"
            )
        return family
    @staticmethod
    def get_family_by_name(db: Session, name: str):
        family = db.query(Family).filter(Family.name == name).first()
        if not family:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Family not found"
            )
        return family
    @staticmethod
    def update_family(db: Session, family_id: str, family_data: FamilyUpdate):
        family = db.query(Family).filter(Family.id == family_id).first()
        if not family:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Family not found"
            )

        # 更新家庭名称
        if family_data.name:
            family.name = family_data.name

        db.commit()
        db.refresh(family)
        return family
    @staticmethod
    def delete_family(db: Session, family_id: str):
        family = db.query(Family).filter(Family.id == family_id).first()
        if not family:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Family not found"
            )

        db.delete(family)
        db.commit()
        return {"message": "Family deleted successfully"}
    @staticmethod
    def add_user_to_family(db: Session, family_id: str, user_id: str):
        # 检查家庭是否存在
        family = db.query(Family).filter(Family.id == family_id).first()
        if not family:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Family not found"
            )

        # 检查用户是否存在
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # 检查用户是否已经属于其他家庭
        if user.family_id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already belongs to a family"
            )

        # 将用户添加到家庭
        user.family_id = family_id
        db.commit()
        db.refresh(user)
        return user
    @staticmethod
    def remove_user_from_family(db: Session, user_id: str):
        # 检查用户是否存在
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # 检查用户是否属于某个家庭
        if user.family_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not belong to any family"
            )

        # 将用户从家庭中移除
        user.family_id = None
        db.commit()
        db.refresh(user)
        return user
    @staticmethod
    def change_user_family(db: Session, user_id: str, new_family_id: str):
        # 检查用户是否存在
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # 检查新家庭是否存在
        new_family = db.query(Family).filter(Family.id == new_family_id).first()
        if not new_family:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="New family not found"
            )

        # 将用户更换到新家庭
        user.family_id = new_family_id
        db.commit()
        db.refresh(user)
        return user