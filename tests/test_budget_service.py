import unittest

from models.budget import Budget
from services.budget_service import BudgetService


class BudgetServiceTest(unittest.TestCase):
    """Test budget workflow rules owned by BudgetService."""

    def setUp(self):
        """Create a fresh service for each test."""
        self.budget = Budget()
        self.service = BudgetService(self.budget)

    def add_money(self, amount=100):
        """Add money and fail fast if the setup step does not work."""
        self.assertTrue(self.service.add_money(amount))

    def create_envelope(self, name="Food", limit=50):
        """Create an envelope and return it."""
        self.assertTrue(self.service.create_envelope(name, limit))
        return self.budget.get_envelopes()[-1]

    def test_add_money_increases_unassigned_money(self):
        self.assertTrue(self.service.add_money(100))

        self.assertEqual(100, self.budget.get_money_available())

    def test_add_money_rejects_zero_and_negative_amounts(self):
        self.assertFalse(self.service.add_money(0))
        self.assertFalse(self.service.add_money(-10))

        self.assertEqual(0, self.budget.get_money_available())

    def test_create_envelope_uses_unassigned_money(self):
        self.add_money(100)

        envelope = self.create_envelope("Food", 40)

        self.assertEqual("Food", envelope.get_name())
        self.assertEqual(40, envelope.get_monthly_limit())
        self.assertEqual(40, envelope.get_current_limit())
        self.assertEqual(60, self.budget.get_money_available())

    def test_create_envelope_rejects_blank_name(self):
        self.add_money(100)

        self.assertFalse(self.service.create_envelope("   ", 40))
        self.assertEqual([], self.budget.get_envelopes())
        self.assertEqual(100, self.budget.get_money_available())

    def test_create_envelope_rejects_duplicate_name_case_insensitively(self):
        self.add_money(100)
        self.create_envelope("Food", 40)

        self.assertFalse(self.service.create_envelope("food", 10))
        self.assertEqual(1, len(self.budget.get_envelopes()))
        self.assertEqual(60, self.budget.get_money_available())

    def test_create_envelope_rejects_invalid_limit(self):
        self.add_money(100)

        self.assertFalse(self.service.create_envelope("Food", 0))
        self.assertFalse(self.service.create_envelope("Gas", -10))
        self.assertFalse(self.service.create_envelope("Rent", 101))
        self.assertEqual([], self.budget.get_envelopes())
        self.assertEqual(100, self.budget.get_money_available())

    def test_has_money_available_and_contains_envelopes(self):
        self.assertFalse(self.service.has_money_available())
        self.assertFalse(self.service.contains_envelopes())

        self.add_money(100)
        self.assertTrue(self.service.has_money_available())

        self.create_envelope("Food", 40)
        self.assertTrue(self.service.contains_envelopes())

    def test_record_expense_adds_expense_to_envelope(self):
        self.add_money(100)
        envelope = self.create_envelope("Food", 40)

        self.assertTrue(
            self.service.record_expense("Groceries", 15, envelope.get_id(), "2026-08-01")
        )

        self.assertEqual(1, len(envelope.get_expenses()))
        self.assertEqual(15, envelope.get_total_spent())
        self.assertEqual(25, envelope.get_remaining())
        self.assertEqual(envelope.get_id(), envelope.get_expenses()[0].get_envelope_id())
        self.assertEqual("2026-08-01", envelope.get_expenses()[0].get_date())

    def test_record_expense_rejects_invalid_inputs(self):
        self.add_money(100)
        envelope = self.create_envelope("Food", 40)

        self.assertFalse(self.service.record_expense("", 10, envelope.get_id()))
        self.assertFalse(self.service.record_expense("Groceries", 0, envelope.get_id()))
        self.assertFalse(self.service.record_expense("Groceries", -1, envelope.get_id()))
        self.assertFalse(self.service.record_expense("Groceries", 41, envelope.get_id()))
        self.assertFalse(self.service.record_expense("Groceries", 10, "missing-id"))
        self.assertEqual([], envelope.get_expenses())

    def test_move_money_between_envelopes(self):
        self.add_money(100)
        food = self.create_envelope("Food", 40)
        gas = self.create_envelope("Gas", 20)

        self.assertTrue(self.service.move_money(food.get_id(), gas.get_id(), 15))

        self.assertEqual(25, food.get_current_limit())
        self.assertEqual(35, gas.get_current_limit())
        self.assertEqual(40, self.budget.get_money_available())

    def test_move_money_allows_moving_exact_remaining_amount(self):
        self.add_money(100)
        food = self.create_envelope("Food", 40)
        gas = self.create_envelope("Gas", 20)
        self.assertTrue(self.service.record_expense("Groceries", 10, food.get_id()))

        self.assertTrue(self.service.move_money(food.get_id(), gas.get_id(), 30))

        self.assertEqual(10, food.get_current_limit())
        self.assertEqual(50, gas.get_current_limit())
        self.assertEqual(0, food.get_remaining())

    def test_move_money_rejects_invalid_moves(self):
        self.add_money(100)
        food = self.create_envelope("Food", 40)
        gas = self.create_envelope("Gas", 20)

        self.assertFalse(self.service.move_money(food.get_id(), food.get_id(), 10))
        self.assertFalse(self.service.move_money(food.get_id(), gas.get_id(), 0))
        self.assertFalse(self.service.move_money(food.get_id(), gas.get_id(), -10))
        self.assertFalse(self.service.move_money(food.get_id(), gas.get_id(), 41))
        self.assertFalse(self.service.move_money("missing-id", gas.get_id(), 10))
        self.assertFalse(self.service.move_money(food.get_id(), "missing-id", 10))
        self.assertEqual(40, food.get_current_limit())
        self.assertEqual(20, gas.get_current_limit())

    def test_edit_envelope_renames_envelope(self):
        self.add_money(100)
        envelope = self.create_envelope("Food", 40)

        self.assertTrue(self.service.edit_envelope(envelope.get_id(), "Groceries"))

        self.assertEqual("Groceries", envelope.get_name())

    def test_edit_envelope_rejects_invalid_names(self):
        self.add_money(100)
        food = self.create_envelope("Food", 40)
        gas = self.create_envelope("Gas", 20)

        self.assertFalse(self.service.edit_envelope(food.get_id(), ""))
        self.assertFalse(self.service.edit_envelope(gas.get_id(), "food"))
        self.assertFalse(self.service.edit_envelope("missing-id", "Travel"))
        self.assertEqual("Food", food.get_name())
        self.assertEqual("Gas", gas.get_name())

    def test_edit_expense_updates_description_and_amount(self):
        self.add_money(100)
        envelope = self.create_envelope("Food", 50)
        self.assertTrue(self.service.record_expense("Coffee", 5, envelope.get_id()))
        expense = envelope.get_expenses()[0]

        self.assertTrue(self.service.edit_expense(expense.get_id(), "Lunch", 20))

        self.assertEqual("Lunch", expense.get_description())
        self.assertEqual(20, expense.get_amount())
        self.assertEqual(30, envelope.get_remaining())

    def test_edit_expense_allows_current_amount_when_envelope_has_no_remaining(self):
        self.add_money(100)
        envelope = self.create_envelope("Food", 50)
        self.assertTrue(self.service.record_expense("Groceries", 50, envelope.get_id()))
        expense = envelope.get_expenses()[0]

        self.assertTrue(self.service.edit_expense(expense.get_id(), "Groceries again", 50))

        self.assertEqual("Groceries again", expense.get_description())
        self.assertEqual(50, expense.get_amount())

    def test_edit_expense_rejects_invalid_updates(self):
        self.add_money(100)
        envelope = self.create_envelope("Food", 50)
        self.assertTrue(self.service.record_expense("Coffee", 5, envelope.get_id()))
        expense = envelope.get_expenses()[0]

        self.assertFalse(self.service.edit_expense(expense.get_id(), "", 10))
        self.assertFalse(self.service.edit_expense(expense.get_id(), "Lunch", 0))
        self.assertFalse(self.service.edit_expense(expense.get_id(), "Lunch", -1))
        self.assertFalse(self.service.edit_expense(expense.get_id(), "Lunch", 51))
        self.assertFalse(self.service.edit_expense("missing-id", "Lunch", 10))
        self.assertEqual("Coffee", expense.get_description())
        self.assertEqual(5, expense.get_amount())

    def test_reset_budget_restores_limits_and_clears_expenses(self):
        self.add_money(100)
        food = self.create_envelope("Food", 40)
        gas = self.create_envelope("Gas", 20)
        self.assertTrue(self.service.record_expense("Groceries", 10, food.get_id()))
        self.assertTrue(self.service.move_money(food.get_id(), gas.get_id(), 10))

        self.service.reset_budget()

        self.assertEqual(40, food.get_monthly_limit())
        self.assertEqual(40, food.get_current_limit())
        self.assertEqual(20, gas.get_monthly_limit())
        self.assertEqual(20, gas.get_current_limit())
        self.assertEqual([], food.get_expenses())
        self.assertEqual(40, self.budget.get_money_available())

    def test_find_envelope_methods(self):
        self.add_money(100)
        envelope = self.create_envelope("Food", 40)

        self.assertIs(envelope, self.service.find_envelope("Food"))
        self.assertIs(envelope, self.service.find_envelope_by_id(envelope.get_id()))
        self.assertIsNone(self.service.find_envelope("Missing"))
        self.assertIsNone(self.service.find_envelope_by_id("missing-id"))


if __name__ == "__main__":
    unittest.main()
