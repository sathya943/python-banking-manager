import functools
import time
from typing import Callable, TypeVar, Any, cast
from collections.abc import Mapping

# Placeholder global security state simulating an active system session context
CURRENT_SESSION: dict[str, Any] = {
    "username": "Esarapu Praveen Kumar",
    "role": "Customer",  # Roles: "Guest", "Customer", "Admin"
    "is_authenticated": True
}

F = TypeVar('F', bound=Callable[..., Any])

def require_role(required_role: str) -> Callable[[F], F]:
    """
    Parameterized Decorator enforcing access security controls based on active session states.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not CURRENT_SESSION.get("is_authenticated"):
                raise PermissionError("Access Denied: User session is unauthenticated.")
            
            user_role = CURRENT_SESSION.get("role")
            if user_role != required_role and user_role != "Admin":
                raise PermissionError(
                    f"Access Denied: Required role '{required_role}' mismatch with current role '{user_role}'."
                )
            
            return func(*args, **kwargs)
        return cast(F, wrapper)
    return decorator


def audit_ledger(func: F) -> F:
    """
    Standard Decorator acting as an Aspect-Oriented automated transaction auditor.
    Logs execution times, method contexts, and operational outcomes.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        method_name = func.__name__
        
        # Extract readable string context if executed bound to a class instance
        instance_repr = str(args[0]) if args else "Global Context"
        
        print(f"🔒 [AUDIT LEDGER ALERT] - {timestamp} - Initiating: {method_name} on {instance_repr}")
        
        try:
            result = func(*args, **kwargs)
            print(f"✅ [AUDIT LEDGER SUCCESS] - Completed: {method_name} successfully execution.")
            return result
        except Exception as err:
            print(f"❌ [AUDIT LEDGER FAILURE] - Caught Exception in '{method_name}': {type(err).__name__} -> {err}")
            raise err  # Re-raise so the application domain can manage it natively
            
    return cast(F, wrapper)