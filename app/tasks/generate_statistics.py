#统计任务
from celery import shared_task
from sqlalchemy.orm import Session
from ..models import Transaction, DailyStat
from ..dependencies import get_db

@shared_task
def generate_statistics(transaction_id):
    with get_db() as db:
        transaction = db.query(Transaction).get(transaction_id)
        
        # 更新日统计
        daily_stat = db.query(DailyStat).filter(
            DailyStat.date == transaction.timestamp.date()
        ).first()
        
        if not daily_stat:
            daily_stat = DailyStat(date=transaction.timestamp.date())
            db.add(daily_stat)
        
        daily_stat.total += transaction.amount
        db.commit()