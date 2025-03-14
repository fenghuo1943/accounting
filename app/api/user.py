from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserRead, UserUpdate
from ..services.user import UserService
from ..dependencies import get_db
from uuid import UUID

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    return UserService.create_user(db, user_data)

@router.get("/id/{user_id}", response_model=UserRead)
def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user
@router.get("/name/{username}", response_model=UserRead)
def get_user_by_username(
    username: str,
    db: Session = Depends(get_db)
):
    try:
        user = UserService.get_user_by_username(db, username)  # 正确传递参数
    except HTTPException as e:
        raise e
    return user
# 更新用户
@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str,  # 用户 ID（UUID）
    user_data: UserUpdate,  # 从请求体中获取更新数据
    db: Session = Depends(get_db)
):
    try:
        user = UserService.update_user(db, user_id, user_data)
    except HTTPException as e:
        raise e
    return user

# 删除用户
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,  # 用户 ID（UUID）
    db: Session = Depends(get_db)
):
    try:
        UserService.delete_user(db, user_id)
    except HTTPException as e:
        raise e
    return None