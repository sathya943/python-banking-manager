class BankingException(Exception):
    """Base exception for all errors within our banking ecosystem."""
    pass

class InsufficientFundsError(BankingException):
    """Raised when an account attempts a withdrawal exceeding its permitted limits."""
    def __init__(self, account_number: str, balance: float, attempted_amount: float) -> None:
        super().__init__(
            f"Account {account_number} has insufficient funds. "
            f"Available: ${balance:.2f}, Attempted: ${attempted_amount:.2f}."
        )