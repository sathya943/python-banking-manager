from abc import ABC, abstractmethod
from app.utils.exceptions import InsufficientFundsError

class Account(ABC):
    def __init__(self, account_number: str, initial_balance: float) -> None:
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.account_number: str = account_number
        self._balance: float = initial_balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        """
        Abstract method. Now raises InsufficientFundsError instead of returning a bool,
        aligning with standard production exception-handling architectures.
        """
        pass

    # --- Dunder (Magic) Methods ---
    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"{self.__class__.__name__}(Acc No: {self.account_number}, Balance: ${self._balance:.2f})"

    def __repr__(self) -> str:
        """Unambiguous developer-focused string representation."""
        return f"Account(account_number='{self.account_number}', balance={self._balance})"

    def __eq__(self, other: object) -> bool:
        """Defines structural equality based on the unique account number identifier."""
        if not isinstance(other, Account):
            return NotImplemented
        return self.account_number == other.account_number


class SavingsAccount(Account):
    def __init__(self, account_number: str, initial_balance: float, minimum_balance: float = 500.0) -> None:
        super().__init__(account_number, initial_balance)
        self.minimum_balance: float = minimum_balance

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        
        if self._balance - amount < self.minimum_balance:
            raise InsufficientFundsError(self.account_number, self._balance, amount)
        self._balance -= amount


class CurrentAccount(Account):
    def __init__(self, account_number: str, initial_balance: float, overdraft_limit: float = 1000.0) -> None:
        super().__init__(account_number, initial_balance)
        self.overdraft_limit: float = overdraft_limit

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        
        if self._balance + self.overdraft_limit < amount:
            raise InsufficientFundsError(self.account_number, self._balance, amount)
        self._balance -= amount