from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from ..schemas import AccountCreate, AccountRead, AccountUpdate
from ..services.account import AccountService
from ..dependencies import get_db

router = APIRouter(prefix="/account", tags=["account"])
# 创建账户
@router.post("/", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db)
):
    return AccountService.create_account(db, account_data)
# 查询账户（按 ID）
@router.get("/{account_id}", response_model=AccountRead)
def get_account(
    account_id: str,
    db: Session = Depends(get_db)
):
    service = AccountService()
    account = service.get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="账户不存在")
    return account
# 查询用户的所有账户
@router.get("/user/{user_id}", response_model=list[AccountRead])
def get_accounts_by_user_id(
    user_id: str,  # 用户 ID（字符串形式的 UUID）
    db: Session = Depends(get_db)
):
    try:
        accounts = AccountService.get_accounts_by_user_id(db, user_id)
    except HTTPException as e:
        raise e
    return accounts

# 更新账户
@router.put("/{account_id}", response_model=AccountRead)
def update_account(
    account_id: str,  # 账户 ID（字符串形式的 UUID）
    account_data: AccountUpdate,  # 从请求体中获取更新数据
    db: Session = Depends(get_db)
):
    try:
        account = AccountService.update_account(db, account_id, account_data)
    except HTTPException as e:
        raise e
    return account

# 删除账户
@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: str,  # 账户 ID（字符串形式的 UUID）
    db: Session = Depends(get_db)
):
    try:
        AccountService.delete_account(db, account_id)
    except HTTPException as e:
        raise e
    return None