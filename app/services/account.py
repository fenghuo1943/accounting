from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import Account, User
from uuid import UUID
from ..schemas import AccountCreate, AccountRead, AccountUpdate
import uuid

class AccountService:
    @staticmethod
    def create_account(db: Session, account_data: AccountCreate):
        user = db.query(User).filter(User.id == account_data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        account = Account(
            id=str(uuid.uuid4()),  # 生成 UUID 并转换为字符串
            name=account_data.name,
            type=account_data.type,
            balance=account_data.balance,
            allow_negative=account_data.allow_negative,
            user_id=account_data.user_id
        )
        db.add(account)
        db.commit()
        db.refresh(account)
        return account
    @staticmethod
    def get_account(self, db: Session, account_id: UUID):
        return db.query(Account).filter(Account.id == account_id).first()
    
    @staticmethod
    def get_account_by_id(db: Session, account_id: str):
        # 直接使用字符串形式的 UUID 查询
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        return account

    @staticmethod
    def get_accounts_by_user_id(db: Session, user_id: str):
        # 查询用户的所有账户
        accounts = db.query(Account).filter(Account.user_id == user_id).all()
        return accounts

    @staticmethod
    def update_account(db: Session, account_id: str, account_data: AccountUpdate):
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )

        # 更新账户信息
        if account_data.name:
            account.name = account_data.name
        if account_data.balance:
            account.balance = account_data.balance
        if account_data.allow_negative is not None:
            account.allow_negative = account_data.allow_negative

        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def delete_account(db: Session, account_id: str):
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )

        db.delete(account)
        db.commit()
        return {"message": "Account deleted successfully"}