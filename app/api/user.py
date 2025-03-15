from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserRead, UserUpdate, UserRegister,Token,TokenData
from ..services.user import UserService
from ..dependencies import get_db
from ..core.auth import create_access_token, get_current_user, oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
from uuid import UUID
from ..models.user import User
from datetime import timedelta

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
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserRegister,  # 从请求体中获取用户注册数据
    db: Session = Depends(get_db)  # 通过依赖注入获取数据库会话
):
    return UserService.register_user(db, user_data)
# 用户注册
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserRegister,  # 从请求体中获取用户注册数据
    db: Session = Depends(get_db)  # 通过依赖注入获取数据库会话
):
    return UserService.register_user(db, user_data)

# 用户登录
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),  # 从表单中获取用户名和密码
    db: Session = Depends(get_db)
):
    user = UserService.get_user_by_username(db, form_data.username)
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成访问令牌
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 获取当前用户信息
@router.get("/me", response_model=UserRead)
def get_current_user_info(
    current_user: User = Depends(get_current_user)  # 确保用户已登录
):
    return current_user