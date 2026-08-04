from datetime import date
import json
import tempfile
import unittest
from pathlib import Path

from models.budget import Budget
from models.envelope import Envelope
from models.expense import Expense
from repositories.budget_repository import BudgetRepository


class BudgetRepositoryTest(unittest.TestCase):
    """Test JSON persistence for budgets."""

    def test_load_budget_returns_new_budget_when_file_is_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "missing.json"
            repository = BudgetRepository(file_path)

            budget = repository.load_budget()

            self.assertIsInstance(budget, Budget)
            self.assertEqual(0, budget.get_money_available())
            self.assertEqual([], budget.get_envelopes())
            self.assertFalse(file_path.exists())

    def test_save_budget_creates_json_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "budget.json"
            repository = BudgetRepository(file_path)
            budget = Budget(id="budget-1", money_available=100)

            repository.save_budget(budget)

            self.assertTrue(file_path.exists())
            with file_path.open("r") as file:
                data = json.load(file)

            self.assertEqual("budget-1", data["id"])
            self.assertEqual(100, data["money_available"])
            self.assertEqual([], data["envelopes"])

    def test_save_and_load_budget_preserves_budget_fields(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "budget.json"
            repository = BudgetRepository(file_path)
            budget = Budget(id="budget-1", money_available=75)

            repository.save_budget(budget)
            loaded_budget = repository.load_budget()

            self.assertEqual("budget-1", loaded_budget.get_id())
            self.assertEqual(75, loaded_budget.get_money_available())
            self.assertEqual([], loaded_budget.get_envelopes())

    def test_save_and_load_budget_preserves_envelopes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "budget.json"
            repository = BudgetRepository(file_path)
            envelope = Envelope(
                "Food",
                50,
                id="env-1",
                current_limit=35,
            )
            budget = Budget(id="budget-1", money_available=25, envelopes=[envelope])

            repository.save_budget(budget)
            loaded_budget = repository.load_budget()
            loaded_envelope = loaded_budget.get_envelopes()[0]

            self.assertEqual("env-1", loaded_envelope.get_id())
            self.assertEqual("Food", loaded_envelope.get_name())
            self.assertEqual(50, loaded_envelope.get_monthly_limit())
            self.assertEqual(35, loaded_envelope.get_current_limit())

    def test_save_and_load_budget_preserves_expenses_and_envelope_links(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "budget.json"
            repository = BudgetRepository(file_path)
            expense = Expense(
                "Coffee",
                5,
                "2026-07-30",
                envelope_id="env-1",
                id="exp-1",
            )
            envelope = Envelope(
                "Food",
                50,
                id="env-1",
                expenses=[expense],
            )
            budget = Budget(id="budget-1", money_available=25, envelopes=[envelope])

            repository.save_budget(budget)
            loaded_budget = repository.load_budget()
            loaded_expense = loaded_budget.get_envelopes()[0].get_expenses()[0]

            self.assertEqual("exp-1", loaded_expense.get_id())
            self.assertEqual("Coffee", loaded_expense.get_description())
            self.assertEqual(5, loaded_expense.get_amount())
            self.assertEqual("env-1", loaded_expense.get_envelope_id())
            self.assertEqual("2026-07-30", loaded_expense.get_date())

    def test_save_and_load_budget_preserves_date_objects_as_iso_strings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "budget.json"
            repository = BudgetRepository(file_path)
            expense = Expense(
                "Coffee",
                5,
                date(2026, 8, 1),
                envelope_id="env-1",
                id="exp-1",
            )
            envelope = Envelope(
                "Food",
                50,
                id="env-1",
                expenses=[expense],
            )
            budget = Budget(id="budget-1", money_available=25, envelopes=[envelope])

            repository.save_budget(budget)
            loaded_budget = repository.load_budget()
            loaded_expense = loaded_budget.get_envelopes()[0].get_expenses()[0]

            self.assertEqual("2026-08-01", loaded_expense.get_date())

    def test_load_budget_uses_parent_envelope_id_when_expense_link_is_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "budget.json"
            file_path.write_text(
                json.dumps(
                    {
                        "id": "budget-1",
                        "money_available": 0,
                        "envelopes": [
                            {
                                "id": "env-1",
                                "name": "Food",
                                "monthly_limit": 50,
                                "current_limit": 50,
                                "expenses": [
                                    {
                                        "id": "exp-1",
                                        "description": "Coffee",
                                        "amount": 5,
                                        "date": None,
                                    }
                                ],
                            }
                        ],
                    }
                )
            )
            repository = BudgetRepository(file_path)

            loaded_budget = repository.load_budget()
            loaded_expense = loaded_budget.get_envelopes()[0].get_expenses()[0]

            self.assertEqual("env-1", loaded_expense.get_envelope_id())

    def test_load_budget_raises_error_for_invalid_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "budget.json"
            file_path.write_text("{not valid json")
            repository = BudgetRepository(file_path)

            with self.assertRaises(json.JSONDecodeError):
                repository.load_budget()


if __name__ == "__main__":
    unittest.main()
