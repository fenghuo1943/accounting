#账单接口
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import TransactionCreate, TransactionRead, TransactionUpdate
from ..services.transaction import TransactionService
from ..exceptions import InsufficientBalanceError 
from ..core.auth import  get_current_user
from ..models.user import User
from ..dependencies import get_db
from uuid import UUID


router = APIRouter(prefix="/transaction", tags=["transaction"])
# 创建账单
@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 确保用户已登录
):
    try:
        return TransactionService.create_transaction(db, transaction_data)
    except InsufficientBalanceError:
        raise HTTPException(status_code=400, detail="账户余额不足")
    
# 查询账单（按 ID）
@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    try:
        transaction = TransactionService.get_transaction_by_id(db, transaction_id)
    except HTTPException as e:
        raise e
    return transaction
@router.get("/account/{account_id}", response_model=list[TransactionRead])
def get_transactions_by_account_id(
    account_id: str,  # 账户 ID（字符串形式的 UUID）
    db: Session = Depends(get_db)
):
    try:
        transactions = TransactionService.get_transactions_by_account_id(db, account_id)
    except HTTPException as e:
        raise e
    return transactions
# 查询用户的所有账单
@router.get("/user/{user_id}", response_model=list[TransactionRead])
def get_transactions_by_user_id(
    user_id: str,  # 用户 ID（字符串形式的 UUID）
    db: Session = Depends(get_db)
):
    try:
        transactions = TransactionService.get_transactions_by_user_id(db, user_id)
    except HTTPException as e:
        raise e
    return transactions

# 更新账单
@router.put("/{transaction_id}", response_model=TransactionRead)
def update_transaction(
    transaction_id: str,  # 账单 ID（字符串形式的 UUID）
    transaction_data: TransactionUpdate,  # 从请求体中获取更新数据
    db: Session = Depends(get_db)
):
    try:
        transaction = TransactionService.update_transaction(db, transaction_id, transaction_data)
    except HTTPException as e:
        raise e
    return transaction

# 删除账单
@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: str,  # 账单 ID（字符串形式的 UUID）
    db: Session = Depends(get_db)
):
    try:
        TransactionService.delete_transaction(db, transaction_id)
    except HTTPException as e:
        raise e
    return None