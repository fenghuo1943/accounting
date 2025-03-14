from fastapi import status
from datetime import datetime
from accounting.app.models.account import Account
from accounting.app.models.transaction import Transaction

def test_create_transaction(client, test_db):
    # 创建一个测试账户
    test_account = Account(user_id=1, balance=1000.0, allow_negative=False)
    test_db.add(test_account)
    test_db.commit()

    # 创建交易请求
    transaction_data = {
        "type": "expense",
        "amount": 100.0,
        "from_account_id": test_account.id
    }

    # 发送请求
    response = client.post("/transactions", json=transaction_data)

    # 验证响应
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["type"] == "expense"
    assert response_data["amount"] == 100.0
    assert response_data["from_account_id"] == test_account.id

    # 验证数据库中的交易记录
    transaction = test_db.query(Transaction).filter(Transaction.id == response_data["id"]).first()
    assert transaction is not None
    assert transaction.amount == 100.0

    # 验证账户余额是否更新
    updated_account = test_db.query(Account).filter(Account.id == test_account.id).first()
    assert updated_account.balance == 900.0