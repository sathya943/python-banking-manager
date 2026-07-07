from app.models.account import SavingsAccount, CurrentAccount, Account
from app.models.customer import Customer

def run_banking_simulation() -> None:
    print("--- Stage 1: Abstraction & OOP Simulation ---")

    # 1. Verify Abstraction prevents direct instantiation of the base class
    try:
        abstract_acc = Account("ACC-000", 100.0)  # type: ignore
    except TypeError as e:
        print(f"Abstraction Working! Blocked instantiating Base Account: {e}\n")

    # 2. Setup Customer and Concrete Accounts
    customer = Customer(customer_id="CUST-777", name="Esarapu Praveen Kumar")
    
    # Savings requires maintaining a $500 minimum balance
    savings = SavingsAccount(account_number="SAV-101", initial_balance=1000.0, minimum_balance=500.0)
    # Current allows a $1000 overdraft limit
    current = CurrentAccount(account_number="CUR-202", initial_balance=200.0, overdraft_limit=1000.0)

    customer.add_account(savings)
    customer.add_account(current)

    print(f"Customer {customer.name} total balance: ${customer.get_total_balance():.2f}")

    # 3. Test customized abstraction behaviors
    print("\nExecuting specialized withdrawal rules:")
    
    # Savings test (Should fail: trying to pull balance below $500)
    savings_success = savings.withdraw(600.0)
    print(f"Savings withdrawal of $600 (Leaves $400, below min $500): Success = {savings_success}")
    print(f"Savings Balance: ${savings.balance:.2f}")

    # Current test (Should pass: utilizes allowed overdraft)
    current_success = current.withdraw(500.0)
    print(f"Current withdrawal of $500 (Overdrafts into -$300): Success = {current_success}")
    print(f"Current Balance: ${current.balance:.2f}")

if __name__ == "__main__":
    run_banking_simulation()