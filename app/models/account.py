from abc import ABC, abstractmethod

class Account(ABC):
    """
    Abstract Base Class (ABC) serving as the blueprint for all bank accounts.
    You cannot instantiate this class directly.
    """
    def __init__(self, account_number: str, initial_balance: float) -> None:
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        
        self.account_number: str = account_number
        self._balance: float = initial_balance

    @property
    def balance(self) -> float:
        """Read-only access to the encapsulated balance."""
        return self._balance

    def deposit(self, amount: float) -> None:
        """Common logic for all accounts: adding positive funds."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount

    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        """
        Abstract method. Every child class MUST implement its own 
        specific withdrawal rules.
        """
        pass


class SavingsAccount(Account):
    """Concrete implementation of an Account with a strict minimum balance rule."""
    def __init__(self, account_number: str, initial_balance: float, minimum_balance: float = 500.0) -> None:
        super().__init__(account_number, initial_balance)
        self.minimum_balance: float = minimum_balance
        
        if initial_balance < minimum_balance:
            raise ValueError(f"Initial balance cannot be lower than minimum balance (${minimum_balance}).")

    def withdraw(self, amount: float) -> bool:
        """Enforces that the balance never drops below the minimum threshold."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        
        # Check if the transaction would violate minimum balance rules
        if self._balance - amount >= self.minimum_balance:
            self._balance -= amount
            return True
        return False


class CurrentAccount(Account):
    """Concrete implementation of an Account that allows a specific overdraft limit."""
    def __init__(self, account_number: str, initial_balance: float, overdraft_limit: float = 1000.0) -> None:
        super().__init__(account_number, initial_balance)
        self.overdraft_limit: float = overdraft_limit

    def withdraw(self, amount: float) -> bool:
        """Allows withdrawals down into the negative overdraft limit."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        
        # Check if total withdrawal fits within balance + overdraft pool
        if self._balance + self.overdraft_limit >= amount:
            self._balance -= amount
            return True
        return False