from typing import List
from app.models.account import Account

class Customer:
    def __init__(self, customer_id: str, name: str) -> None:
        self.customer_id: str = customer_id
        self.name: str = name
        self._accounts: List[Account] = []
    
    def add_account(self, account: Account) -> None:
        self._accounts.append(account)
    
    def get_total_balance(self) -> float:
        return sum(account.balance for account in self._accounts)
    
        