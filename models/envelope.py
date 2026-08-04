"""Envelope model for monthly budget categories."""

from uuid import uuid4
import math


class Envelope: 
    """Represent a budget envelope and its current-month expenses."""

    def __init__(self, name, monthly_limit, id=None, current_limit=None, expenses=None): 
        """Create an envelope.

        Args:
            name: User-facing envelope name.
            monthly_limit: Normal monthly amount restored on reset.
            id: Existing envelope ID when loading saved data.
            current_limit: Current month adjusted amount.
            expenses: Existing expenses when loading saved data.
        """
        self.__id: str = id or str(uuid4())
        self.__name: str = name
        self.__monthly_limit: float = monthly_limit
        self.__current_limit: float = current_limit if current_limit is not None else monthly_limit
        self.__expenses: list = expenses or []


    def set_name(self, name: str): 
        """Set the envelope name when the value is not blank.

        Args:
            name: New envelope name.
        """
        if len(name) > 0:
            self.__name = name

    def get_name(self) -> str: 
        """Return the envelope name."""
        return self.__name
    
    def set_monthly_limit(self, monthly_limit: float): 
        """Set the normal monthly envelope limit.

        Args:
            monthly_limit: New monthly limit.
        """
        self.__monthly_limit = monthly_limit 

    def get_monthly_limit(self) -> float: 
        """Return the normal monthly envelope limit."""
        return self.__monthly_limit

    def set_current_limit(self, current_limit: float): 
        """Set the current month envelope limit.

        Args:
            current_limit: New current month limit.
        """
        self.__current_limit = current_limit 

    def get_current_limit(self) -> float: 
        """Return the current month envelope limit."""
        return self.__current_limit
    
    def increase_current_limit(self, amount: float): 
        """Increase the current month envelope limit.

        Args:
            amount: Amount to add to the current limit.
        """
        self.__current_limit += amount 

    def decrease_current_limit(self, amount: float): 
        """Decrease the current month envelope limit.

        Args:
            amount: Amount to subtract from the current limit.
        """
        self.__current_limit -= amount

    def get_id(self) -> str: 
        """Return the envelope ID."""
        return self.__id

    def get_total_spent(self) -> float: 
        """Return total spending recorded in this envelope."""
        total = 0.0 
        for expense in self.__expenses: 
            total += expense.get_amount()
        return total
    
    def get_remaining(self) -> float: 
        """Return current limit minus total spent."""
        return self.__current_limit - self.get_total_spent()
    
    def get_percent(self) -> float: 
        """Return the percent of the current limit that has been spent."""
        if self.__current_limit == 0:
            return 0
        return math.ceil(self.get_total_spent() / self.__current_limit * 100)
    
    def set_expenses(self, expenses: list): 
        """Replace the envelope's expenses.

        Args:
            expenses: New list of expenses.
        """
        self.__expenses = expenses 

    def get_expenses(self) -> list: 
        """Return expenses recorded in this envelope."""
        return self.__expenses
    
    def record_expense(self, expense): 
        """Add a positive expense to this envelope.

        Args:
            expense: Expense to record.
        """
        if expense.get_amount() > 0:
            self.__expenses.append(expense)

    def get_expense_by_id(self, expense_id: str):
        """Find an expense by ID.

        Args:
            expense_id: ID to search for.

        Returns:
            Matching expense, or None if no expense matches.
        """
        for expense in self.__expenses:
            if expense.get_id() == expense_id:
                return expense
        return None 

    def reset_envelope(self): 
        """Restore current limit and clear current expenses."""
        self.__current_limit = self.__monthly_limit
        self.__expenses = []
        
    def __eq__(self, other): 
        """Return whether another object represents the same envelope values."""
        return isinstance(other, Envelope) and (self.__name == other.get_name()) \
            and (self.__monthly_limit == other.get_monthly_limit())
    
    def __str__(self): 
        """Return a human-readable envelope summary."""
        return (
            f"{self.__name}: ${self.get_total_spent()} / " 
            f"${self.__current_limit} -> {self.get_percent()}% used"
            )
