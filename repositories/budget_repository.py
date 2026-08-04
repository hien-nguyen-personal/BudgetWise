"""JSON repository for loading and saving BudgetWise data."""

import json
from pathlib import Path

from models.budget import Budget
from models.envelope import Envelope
from models.expense import Expense


class BudgetRepository:
    """Persist a budget to a local JSON file."""

    def __init__(self, file_path="budget_data.json"):
        """Create a repository.

        Args:
            file_path: JSON file path used for persistence.
        """
        self.__file_path = Path(file_path)

    def load_budget(self) -> Budget:
        """Load a budget from JSON or return a new budget.

        Returns:
            Saved budget if the data file exists; otherwise a new budget.
        """
        if not self.__file_path.exists():
            return Budget()

        with self.__file_path.open("r") as file:
            data = json.load(file)

        return self.__budget_from_dict(data)

    def save_budget(self, budget: Budget):
        """Save a budget to JSON.

        Args:
            budget: Budget object to persist.
        """
        data = self.__budget_to_dict(budget)

        with self.__file_path.open("w") as file:
            json.dump(data, file, indent=2)

    def __budget_to_dict(self, budget: Budget) -> dict:
        """Convert a Budget object into a JSON-ready dictionary."""
        return {
            "id": budget.get_id(),
            "money_available": budget.get_money_available(),
            "envelopes": [
                self.__envelope_to_dict(envelope)
                for envelope in budget.get_envelopes()
            ],
        }

    def __envelope_to_dict(self, envelope: Envelope) -> dict:
        """Convert an Envelope object into a JSON-ready dictionary."""
        return {
            "id": envelope.get_id(),
            "name": envelope.get_name(),
            "monthly_limit": envelope.get_monthly_limit(),
            "current_limit": envelope.get_current_limit(),
            "expenses": [
                self.__expense_to_dict(expense)
                for expense in envelope.get_expenses()
            ],
        }

    def __expense_to_dict(self, expense: Expense) -> dict:
        """Convert an Expense object into a JSON-ready dictionary."""
        expense_date = expense.get_date()

        if hasattr(expense_date, "isoformat"):
            expense_date = expense_date.isoformat()

        return {
            "id": expense.get_id(),
            "description": expense.get_description(),
            "amount": expense.get_amount(),
            "envelope_id": expense.get_envelope_id(),
            "date": expense_date,
        }

    def __budget_from_dict(self, data: dict) -> Budget:
        """Build a Budget object from saved dictionary data."""
        budget = Budget(
            id=data.get("id"),
            money_available=data.get("money_available", 0),
        )

        envelopes = [
            self.__envelope_from_dict(envelope_data)
            for envelope_data in data.get("envelopes", [])
        ]
        budget.set_envelopes(envelopes)

        return budget

    def __envelope_from_dict(self, data: dict) -> Envelope:
        """Build an Envelope object from saved dictionary data."""
        envelope = Envelope(
            data.get("name", ""),
            data.get("monthly_limit", 0),
            id=data.get("id"),
            current_limit=data.get("current_limit"),
        )

        expenses = [
            self.__expense_from_dict(expense_data, envelope.get_id())
            for expense_data in data.get("expenses", [])
        ]
        envelope.set_expenses(expenses)

        return envelope

    def __expense_from_dict(self, data: dict, envelope_id: str) -> Expense:
        """Build an Expense object from saved dictionary data."""
        return Expense(
            data.get("description", ""),
            data.get("amount", 0),
            data.get("date"),
            data.get("envelope_id") or envelope_id,
            id=data.get("id"),
        )
