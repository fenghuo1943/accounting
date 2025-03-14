from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from ..schemas import FamilyCreate,FamilyRead,FamilyUpdate, UserRead
from ..services.family import FamilyService
from ..dependencies import get_db
from uuid import UUID

router = APIRouter(prefix="/family", tags=["family"])

@router.post("/", response_model=FamilyRead, status_code=status.HTTP_201_CREATED)
def create_family(
    family_data: FamilyCreate,
    db: Session = Depends(get_db)
):
    return FamilyService().create_family(db, family_data)

# 查询家庭（按 ID）
@router.get("/id/{family_id}", response_model=FamilyRead)
def get_family(
    family_id: str,  # 家庭 ID（UUID）
    db: Session = Depends(get_db)
):
    try:
        family = FamilyService.get_family_by_id(db, family_id)
    except HTTPException as e:
        raise e
    return family

# 查询家庭（按名称）
@router.get("/name/{name}", response_model=FamilyRead)
def get_family_by_name(
    name: str,  # 家庭名称
    db: Session = Depends(get_db)
):
    try:
        family = FamilyService.get_family_by_name(db, name)
    except HTTPException as e:
        raise e
    return family

# 更新家庭
@router.put("/{family_id}", response_model=FamilyRead)
def update_family(
    family_id: str,  # 家庭 ID（UUID）
    family_data: FamilyUpdate,  # 从请求体中获取更新数据
    db: Session = Depends(get_db)
):
    try:
        family = FamilyService.update_family(db, family_id, family_data)
    except HTTPException as e:
        raise e
    return family

# 删除家庭
@router.delete("/{family_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_family(
    family_id: str,  # 家庭 ID（UUID）
    db: Session = Depends(get_db)
):
    try:
        FamilyService.delete_family(db, family_id)
    except HTTPException as e:
        raise e
    return None

# 用户加入家庭
@router.post("/{family_id}/user/{user_id}", response_model=UserRead)
def add_user_to_family(
    family_id: str,  # 家庭 ID（UUID）
    user_id: str,  # 用户 ID（UUID）
    db: Session = Depends(get_db)
):
    try:
        user = FamilyService.add_user_to_family(db, family_id, user_id)
    except HTTPException as e:
        raise e
    return user

@router.post("/user/{user_id}/remove", response_model=UserRead)
def remove_user_from_family(
    user_id: str,  # 用户 ID（字符串形式的 UUID）
    db: Session = Depends(get_db)
):
    try:
        user = FamilyService.remove_user_from_family(db, user_id)
    except HTTPException as e:
        raise e
    return user

@router.post("/user/{user_id}/change_family", response_model=UserRead)
def change_user_family(
    user_id: str,  # 用户 ID（字符串形式的 UUID）
    new_family_id: str,  # 新家庭 ID（字符串形式的 UUID）
    db: Session = Depends(get_db)
):
    try:
        user = FamilyService.change_user_family(db, user_id, new_family_id)
    except HTTPException as e:
        raise e
    return user