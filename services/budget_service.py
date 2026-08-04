from models.budget import Budget
from models.expense import Expense
from models.envelope import Envelope


class BudgetService: 
    """Coordinate budget workflows and enforce business rules."""

    def __init__(self, budget: Budget): 
        """Create a service for an existing budget.

        Args:
            budget: Budget object managed by this service.
        """
        self.__budget = budget

    def get_budget(self) -> Budget: 
        """Return the budget managed by this service."""
        return self.__budget

    def set_budget(self, budget: Budget): 
        """Replace the budget managed by this service.

        Args:
            budget: New budget object to manage.
        """
        self.__budget = budget

    def create_envelope(self, name: str, limit: float) -> bool: 
        """Create an envelope and fund it from unassigned money.

        Args:
            name: Envelope name entered by the user.
            limit: Monthly/current limit for the new envelope.

        Returns:
            True if the envelope was created; otherwise False.
        """
        name = name.strip()

        if not self._is_valid_name(name):
            return False

        if not self._is_unique_envelope_name(name):
            return False

        if not self._is_positive_amount(limit):
            return False

        if not self._has_enough_available_money(limit):
            return False

        envelope = Envelope(name, limit)
        self.__budget.add_envelope(envelope)
        self.__budget.decrease_money_available(limit)
        return True
    
    def delete_envelope(self, envelope_id: str) -> bool:
        """Delete an existing envelope. 

        Args: 
            envelope_id: ID of the envelope to delete. 

        Returns: 
            True if the envelope was delete; otherwise False.
        """
        envelope = self.find_envelope_by_id(envelope_id)
        
        if not envelope: 
            return False
        
        self.__budget.delete_envelope(envelope)
        return True

    def edit_envelope(self, envelope_id: str, name: str) -> bool:
        """Rename an existing envelope.

        Args:
            envelope_id: ID of the envelope to rename.
            name: New envelope name.

        Returns:
            True if the envelope was renamed; otherwise False.
        """
        envelope = self.find_envelope_by_id(envelope_id)
        name = name.strip()

        if not envelope:
            return False

        if not self._is_valid_name(name):
            return False

        if not self._is_unique_envelope_name(name, envelope_id):
            return False

        envelope.set_name(name)
        return True

    def _has_enough_available_money(self, amount) -> bool:
        """Return whether unassigned money can cover an amount."""
        return amount <= self.__budget.get_money_available()

    def _is_unique_envelope_name(self, name: str, current_envelope_id=None) -> bool:
        """Return whether an envelope name is unused.

        Args:
            name: Envelope name to check.
            current_envelope_id: Envelope ID to ignore during rename checks.

        Returns:
            True if no other envelope has the same name; otherwise False.
        """
        for envelope in self.__budget.get_envelopes():
            if envelope.get_id() == current_envelope_id:
                continue

            if envelope.get_name().lower() == name.lower():
                return False

        return True

    def _is_valid_name(self, name: str) -> bool:
        """Return whether a text field has non-blank content."""
        return len(name.strip()) > 0

    def _find_expense_and_envelope(self, expense_id: str):
        """Find an expense and the envelope that owns it.

        Args:
            expense_id: ID of the expense to find.

        Returns:
            A tuple of (envelope, expense), or False if not found.
        """
        for envelope in self.__budget.get_envelopes():
            expense = envelope.get_expense_by_id(expense_id)
            if expense:
                return envelope, expense

        return False
    
    def has_money_available(self) -> bool: 
        """Return whether the budget has unassigned money."""
        return self._is_positive_amount(self.__budget.get_money_available())
    
    def _is_valid_limit(self, limit) -> bool: 
        """Return whether a new envelope limit can be funded."""
        return self._is_positive_amount(limit) and self._has_enough_available_money(limit)

    def add_money(self, money: float) -> bool: 
        """Add money to the budget's unassigned money.

        Args:
            money: Amount to add.

        Returns:
            True if money was added; otherwise False.
        """
        if self._is_positive_amount(money): 
            self.__budget.add_money(money)
            return True
        return False

    def record_expense(self, description: str, amount: float, envelope_id: str, expense_date=None) -> bool:
        """Record a new expense in an envelope.

        Args:
            description: Expense description.
            amount: Expense amount.
            envelope_id: ID of the envelope receiving the expense.
            expense_date: Date the expense happened.

        Returns:
            True if the expense was recorded; otherwise False.
        """
        envelope = self.find_envelope_by_id(envelope_id)
        description = description.strip()

        if not envelope:
            return False

        if not self._is_valid_name(description):
            return False

        if not self._is_positive_amount(amount):
            return False

        if envelope.get_remaining() < amount:
            return False

        expense = Expense(description, amount, expense_date, envelope.get_id())
        envelope.record_expense(expense)
        return True
    
    def edit_expense(self, expense_id: str, description: str, amount: float) -> bool:
        """Update an expense description and amount.

        Args:
            expense_id: ID of the expense to update.
            description: New expense description.
            amount: New expense amount.

        Returns:
            True if the expense was updated; otherwise False.
        """
        result = self._find_expense_and_envelope(expense_id)

        if not result:
            return False

        envelope, expense = result
        description = description.strip()

        if not self._is_valid_name(description):
            return False

        if not self._is_positive_amount(amount):
            return False

        available_after_removing_current_expense = envelope.get_remaining() + expense.get_amount()
        if available_after_removing_current_expense < amount:
            return False

        expense.set_description(description)
        expense.set_amount(amount)
        return True
    
    def _is_positive_amount(self, amount) -> bool: 
        """Return whether an amount is greater than zero."""
        return amount is not None and amount > 0

    
    def find_envelope(self, envelope_name: str) -> Envelope: 
        """Find an envelope by name.

        Args:
            envelope_name: Name to search for.

        Returns:
            Matching envelope, or None if no envelope matches.
        """
        return self.__budget.get_envelope_by_name(envelope_name)

    def find_envelope_by_id(self, envelope_id: str) -> Envelope:
        """Find an envelope by ID.

        Args:
            envelope_id: ID to search for.

        Returns:
            Matching envelope, or None if no envelope matches.
        """
        return self.__budget.get_envelope_by_id(envelope_id)
    
    def contains_envelopes(self) -> bool: 
        """Return whether the budget currently has any envelopes."""
        return len(self.__budget.get_envelopes()) > 0
    
    def move_money(self, from_envelope_id: str, to_envelope_id: str, amount: float) -> bool: 
        """Move money between two envelopes' current limits.

        Args:
            from_envelope_id: ID of the source envelope.
            to_envelope_id: ID of the target envelope.
            amount: Amount to move.

        Returns:
            True if money was moved; otherwise False.
        """
        if from_envelope_id == to_envelope_id:
            return False

        if not self._is_positive_amount(amount):
            return False

        return self.__budget.move_money(from_envelope_id, to_envelope_id, amount)
    
    def get_available_money_from_envelopes(self) -> str: 
        """Build a display string showing each envelope's remaining money."""
        result = "Available money per envelope: \n"
        envelopes = self.__budget.get_envelopes()
        for index, envelope in enumerate(envelopes): 
            result += f"{index+1}. {envelope.get_name()}: ${envelope.get_remaining()} \n"
        return result
    
    def reset_budget(self): 
        """Reset all envelopes for a new budget month."""
        self.__budget.reset_budget()
    
    def get_summary(self): 
        """Return a display string for the current budget summary."""
        return "Budget: \n" + f"{self.__budget}"
