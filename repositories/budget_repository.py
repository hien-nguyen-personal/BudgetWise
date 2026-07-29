import json
from pathlib import Path

from models.budget import Budget
from models.envelope import Envelope
from models.expense import Expense


class BudgetRepository:
    def __init__(self, file_path="budget_data.json"):
        self.__file_path = Path(file_path)

    def load_budget(self) -> Budget:
        if not self.__file_path.exists():
            return Budget()

        with self.__file_path.open("r") as file:
            data = json.load(file)

        return self.__budget_from_dict(data)

    def save_budget(self, budget: Budget):
        data = self.__budget_to_dict(budget)

        with self.__file_path.open("w") as file:
            json.dump(data, file, indent=2)

    def __budget_to_dict(self, budget: Budget) -> dict:
        return {
            "id": budget.get_id(),
            "money_available": budget.get_money_available(),
            "envelopes": [
                self.__envelope_to_dict(envelope)
                for envelope in budget.get_envelopes()
            ],
        }

    def __envelope_to_dict(self, envelope: Envelope) -> dict:
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
        return Expense(
            data.get("description", ""),
            data.get("amount", 0),
            data.get("date"),
            data.get("envelope_id") or envelope_id,
            id=data.get("id"),
        )
