from abc import ABC, abstractmethod
from app.utils.exceptions import InsufficientFundsError
from app.decorators.security import audit_ledger, require_role

class Account(ABC):
    def __init__(self, account_number: str, initial_balance: float) -> None:
        self.account_number: str = account_number
        self._balance: float = initial_balance

    @property
    def balance(self) -> float:
        return self._balance

    # Snapping aspects on top of our concrete actions
    @audit_ledger
    @require_role(required_role="Customer")
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        pass

    def __str__(self) -> str:
        return f"Acc ({self.account_number})"


class SavingsAccount(Account):
    @audit_ledger
    @require_role(required_role="Customer")
    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self._balance - amount < 500.0:
            raise InsufficientFundsError(self.account_number, self._balance, amount)
        self._balance -= amount


class CurrentAccount(Account):
    @audit_ledger
    @require_role(required_role="Admin")  # Restricting Current Account withdrawals to Admin oversight
    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self._balance + 1000.0 < amount:
            raise InsufficientFundsError(self.account_number, self._balance, amount)
        self._balance -= amount