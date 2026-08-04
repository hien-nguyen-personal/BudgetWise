"""Budget model for grouping envelopes and unassigned money."""

from models.envelope import Envelope
from uuid import uuid4


class Budget: 
    """Represent one envelope budget."""

    def __init__(self, id=None, money_available=0, envelopes=None): 
        """Create a budget.

        Args:
            id: Existing budget ID when loading saved data.
            money_available: Unassigned money available for envelopes.
            envelopes: Existing envelopes when loading saved data.
        """
        self.__id: str = id or str(uuid4())
        self.__envelopes: list[Envelope] = envelopes or []
        self.__money_available: float = money_available

    def get_id(self) -> str:
        """Return the budget ID."""
        return self.__id

    def set_envelopes(self, envelopes: list[Envelope]): 
        """Replace the budget's envelopes.

        Args:
            envelopes: New list of envelopes.
        """
        self.__envelopes = envelopes 

    def get_envelopes(self) -> list[Envelope]: 
        """Return all envelopes in the budget."""
        return self.__envelopes 
    
    def add_envelope(self, envelope: Envelope): 
        """Add an envelope to the budget.

        Args:
            envelope: Envelope to add.
        """
        self.__envelopes.append(envelope)

    def delete_envelope(self, envelope: Envelope): 
        """Deleve an envelope from the budget. 

        Args: 
        envelope: Envelope to delete.
        """
        self.__envelopes.remove(envelope)
        self.__money_available += envelope.get_current_limit()

    def get_envelope_by_name(self, envelope_name: str) -> Envelope: 
        """Find an envelope by name.

        Args:
            envelope_name: Name to search for.

        Returns:
            Matching envelope, or None if no envelope matches.
        """
        for envelope in self.__envelopes: 
            if envelope.get_name() == envelope_name:
                return envelope 
        return None
    
    def get_envelope_by_id(self, envelope_id: str) -> Envelope: 
        """Find an envelope by ID.

        Args:
            envelope_id: ID to search for.

        Returns:
            Matching envelope, or None if no envelope matches.
        """
        for envelope in self.__envelopes: 
            if envelope.get_id() == envelope_id: 
                return envelope
        return None
    
    def move_money(self, from_envelope_id: str, to_envelope_id: str, amount: int) -> bool: 
        """Move money between two envelopess' current limits. 

        Args: 
            from_envelope_id: ID of the source envelope. 
            to_envelope_id: ID of the target envelope. 
            amount: Amount to move.

        Returns: 
            True if money was moved; otherwise False.
        """
        from_envelope = self.get_envelope_by_id(from_envelope_id)
        to_envelope = self.get_envelope_by_id(to_envelope_id)

        if not from_envelope or not to_envelope: 
            return False 
        
        if from_envelope.get_remaining() < amount: 
            return False 
        
        from_envelope.decrease_current_limit(amount)
        to_envelope.increase_current_limit(amount)
        return True
    
    def get_money_available(self) -> float: 
        """Return unassigned money available for new envelopes."""
        return self.__money_available
    
    def set_money_available(self, money_available: float): 
        """Set unassigned money.

        Args:
            money_available: New unassigned money amount.
        """
        self.__money_available = money_available

    def decrease_money_available(self, amount: float): 
        """Decrease unassigned money.

        Args:
            amount: Amount to subtract.
        """
        self.__money_available -= amount 

    def increase_money_available(self, amount: float): 
        """Increase unassigned money.

        Args:
            amount: Amount to add.
        """
        self.__money_available += amount

    def add_money(self, money: float): 
        """Add money to the budget's unassigned money.

        Args:
            money: Amount to add.
        """
        self.__money_available += money

    def get_total_spent(self) -> float: 
        """Return total spending across all envelopes."""
        total = 0.0
        for envelope in self.__envelopes: 
            total += envelope.get_total_spent()
        return total
    
    def reset_budget(self): 
        """Reset all envelopes for a new month."""
        for envelope in self.__envelopes: 
            envelope.reset_envelope()
    
    def __str__(self): 
        """Return a human-readable budget summary."""
        result = "Money available: " + f"${self.__money_available} \n" 
        result += "Envelopes: \n"
        if len(self.__envelopes) > 0:
            for envelope in self.__envelopes: 
                result += f"{envelope}" + "\n"
        else: 
            result += "No envelopes to display."
        return result
