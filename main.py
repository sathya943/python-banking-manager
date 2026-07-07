from app.models.account import SavingsAccount, CurrentAccount
from app.decorators.security import CURRENT_SESSION
from app.utils.exceptions import BankingException

def run_stage_3_simulation() -> None:
    print("--- Stage 3: Decorators, Security & Audit Logs ---")

    # 1. Initialize core system artifacts
    savings = SavingsAccount("SAV-777", 2000.0)
    current = CurrentAccount("CUR-888", 1500.0)

    # 2. Test standard operational flow under validated user context
    print(f"\nActive Session User: {CURRENT_SESSION['username']} | Role: {CURRENT_SESSION['role']}")
    savings.deposit(500.0)
    savings.withdraw(300.0)

    # 3. Test operational constraint blocking (Current account requires Admin clearance)
    print("\nAttempting unauthorized action on Current Account...")
    try:
        current.withdraw(100.0)
    except PermissionError as err:
        print(f"Security Shield Handled Alert 🛡️ -> {err}")

    # 4. Escalate privileges to simulate an Admin login bypass
    print("\nEscalating session profile state to 'Admin'...")
    CURRENT_SESSION["role"] = "Admin"
    print(f"Updated Session User: {CURRENT_SESSION['username']} | Role: {CURRENT_SESSION['role']}")

    # Re-attempt the transaction
    current.withdraw(100.0)
    
    # 5. Simulate failed transaction tracking to verify the audit ledger caught it
    print("\nSimulating a failing transaction under valid auth permissions...")
    try:
        savings.withdraw(5000.0) # Triggers InsufficientFundsError
    except BankingException:
        pass # Ignored here since the auditor printed the trace stack trace output

if __name__ == "__main__":
    run_stage_3_simulation()