#异常
class InsufficientBalanceError(Exception):
    """
    账户余额不足异常
    """
    def __init__(self, message="账户余额不足"):
        self.message = message
        super().__init__(self.message)