from app.models.account import Account, SavingsAccount, CurrentAccount
from app.utils.exceptions import InsufficientFundsError, BankingException

class BankServiceMesh:
    """Handles system-wide workflows including polymorphic inter-account transfers."""
    
    @staticmethod
    def transfer(sender: Account, receiver: Account, amount: float) -> None:
        """
        Polymorphically transfers funds between ANY two abstract account types.
        Uses Type Hints to ensure proper structural interaction.
        """
        print(f"Initiating transfer: ${amount:.2f} from {sender.account_number} to {receiver.account_number}...")
        
        # If withdraw fails via exception, execution halts automatically, protecting data integrity
        sender.withdraw(amount)
        receiver.deposit(amount)
        print("Transfer completed successfully.")


def run_stage_2_simulation() -> None:
    print("--- Stage 2: Polymorphism, Exceptions & Dunder Methods ---")
    
    # 1. Instantiate Accounts
    sa = SavingsAccount("SAV-999", 1200.0)
    ca = CurrentAccount("CUR-888", 300.0)

    # Testing Dunder Methods (__str__ / __repr__)
    print(f"\nCreated Account (str): {sa}")
    print(f"Created Account (repr): {repr(ca)}")

    # Testing Dunder Equality (__eq__)
    duplicate_check_acc = CurrentAccount("CUR-888", 5000.0)
    print(f"Is target account identical to duplicate account object? {ca == duplicate_check_acc}")

    print("\n--- Executing Safe Polymorphic Transfer ---")
    # Transfer from Savings -> Current (Works perfectly)
    BankServiceMesh.transfer(sender=sa, receiver=ca, amount=400.0)
    print(f"Updated Sender: {sa}")
    print(f"Updated Receiver: {ca}")

    print("\n--- Executing Violating Polymorphic Transfer ---")
    # Transfer from Current -> Savings exceeding overdraft bounds (Should raise customized error)
    try:
        BankServiceMesh.transfer(sender=ca, receiver=sa, amount=1500.0)
    except InsufficientFundsError as err:
        print(f"Caught Domain Specific Exception Alert 🚨 -> {err}")
    except BankingException as err:
        print(f"Caught global banking exception: {err}")

if __name__ == "__main__":
    run_stage_2_simulation()