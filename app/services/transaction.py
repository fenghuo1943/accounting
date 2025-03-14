#账单服务
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import Transaction, Account, User
from ..schemas import TransactionCreate, TransactionRead, TransactionUpdate
from ..exceptions import InsufficientBalanceError
from uuid import UUID
import uuid

class TransactionService:
    @staticmethod
    def create_transaction(db: Session, transaction_data: TransactionCreate):
        # 检查账户是否存在
        account = db.query(Account).filter(Account.id == transaction_data.from_account_id).first
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        # 检查用户是否存在
        user = db.query(User).filter(User.id == transaction_data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # 创建交易对象，生成 UUID 并转换为字符串
        transaction = Transaction(
            id=str(uuid.uuid4()),  # 生成 UUID 并转换为字符串
            type=transaction_data.type,
            amount=transaction_data.amount,
            from_account_id=transaction_data.from_account_id,
            user_id=transaction_data.user_id
        )
        
        # 创建账单
        transaction = Transaction(**transaction_data)
        db.add(transaction)
        
        # 更新账户余额
        account.balance -= transaction_data["amount"]
        db.commit()
        db.refresh(transaction)
        # 触发异步统计任务
        #from ..tasks import generate_statistics
        #generate_statistics.delay(transaction.id)
        
        return transaction
    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: str):
        # 直接使用字符串形式的 UUID 查询
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        return transaction
    @staticmethod
    def get_transactions_by_account_id(db: Session, account_id: str):
        # 检查账户是否存在
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        # 查询账户下的所有账单
        transactions = db.query(Transaction).filter(Transaction.from_account_id == account_id).all()
        return transactions
    @staticmethod
    def get_transactions_by_user_id(db: Session, user_id: str):
        # 查询用户的所有交易
        transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
        return transactions
    
    @staticmethod
    def update_transaction(db: Session, transaction_id: str, transaction_data: TransactionUpdate):
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )

        # 更新交易信息
        if transaction_data.type:
            transaction.type = transaction_data.type
        if transaction_data.amount:
            transaction.amount = transaction_data.amount
        if transaction_data.from_account_id:
            transaction.from_account_id = transaction_data.from_account_id

        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def delete_transaction(db: Session, transaction_id: str):
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )

        db.delete(transaction)
        db.commit()
        return {"message": "Transaction deleted successfully"}