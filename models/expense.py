"""Expense model for spending recorded against an envelope."""

from datetime import date
from uuid import uuid4


class Expense: 
    """Represent one expense transaction."""

    def __init__(self, description, amount, expense_date=None, envelope_id=None, id=None): 
        """Create an expense.

        Args:
            description: User-facing expense description.
            amount: Expense amount.
            expense_date: Date the expense happened.
            envelope_id: ID of the envelope that owns the expense.
            id: Existing expense ID when loading saved data.
        """
        self.__id: str = id or str(uuid4())
        self.__description: str = description 
        self.__amount: float = amount 
        self.__envelope_id: str = envelope_id
        self.__date: date = expense_date

    def get_id(self) -> str:
        """Return the expense ID."""
        return self.__id

    def set_description(self, description): 
        """Set the expense description.

        Args:
            description: New expense description.
        """
        self.__description = description

    def get_description(self): 
        """Return the expense description."""
        return self.__description
    
    def set_amount(self, amount): 
        """Set the expense amount when the value is positive.

        Args:
            amount: New expense amount.
        """
        if amount > 0: 
            self.__amount = amount 

    def get_amount(self): 
        """Return the expense amount."""
        return self.__amount
    
    def set_envelope(self, envelope_id): 
        """Set the ID of the envelope that owns this expense.

        Args:
            envelope_id: New owning envelope ID.
        """
        self.__envelope_id = envelope_id

    def get_envelope_id(self): 
        """Return the ID of the envelope that owns this expense."""
        return self.__envelope_id
    
    def set_date(self, date): 
        """Set the expense date.

        Args:
            date: New expense date.
        """
        self.__date = date 

    def get_date(self): 
        """Return the expense date."""
        return self.__date
    
    def __str__(self): 
        """Return a human-readable expense summary."""
        if self.__date:
            return f"{self.__date} - {self.__description} - ${self.__amount}"

        return f"{self.__description} - ${self.__amount}"
    

    
