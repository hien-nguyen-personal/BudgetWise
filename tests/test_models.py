import unittest

from models.budget import Budget
from models.envelope import Envelope
from models.expense import Expense


class BudgetTest(unittest.TestCase):
    """Test Budget model behavior."""

    def test_budget_generates_id_and_accepts_existing_id(self):
        budget = Budget()
        loaded_budget = Budget(id="budget-1")

        self.assertTrue(budget.get_id())
        self.assertEqual("budget-1", loaded_budget.get_id())

    def test_budget_tracks_unassigned_money(self):
        budget = Budget()

        budget.add_money(100)
        budget.decrease_money_available(30)
        budget.increase_money_available(10)

        self.assertEqual(80, budget.get_money_available())

    def test_budget_manages_envelopes(self):
        budget = Budget()
        envelope = Envelope("Food", 50)

        budget.add_envelope(envelope)

        self.assertEqual([envelope], budget.get_envelopes())
        self.assertIs(envelope, budget.get_envelope_by_name("Food"))
        self.assertIs(envelope, budget.get_envelope_by_id(envelope.get_id()))
        self.assertIsNone(budget.get_envelope_by_name("Missing"))
        self.assertIsNone(budget.get_envelope_by_id("missing-id"))

    def test_budget_total_spent_sums_all_envelopes(self):
        food = Envelope("Food", 50)
        gas = Envelope("Gas", 30)
        food.record_expense(Expense("Groceries", 20, envelope_id=food.get_id()))
        gas.record_expense(Expense("Fuel", 10, envelope_id=gas.get_id()))
        budget = Budget(envelopes=[food, gas])

        self.assertEqual(30, budget.get_total_spent())

    def test_budget_reset_resets_all_envelopes(self):
        food = Envelope("Food", 50)
        gas = Envelope("Gas", 30)
        food.record_expense(Expense("Groceries", 20, envelope_id=food.get_id()))
        food.decrease_current_limit(10)
        gas.increase_current_limit(5)
        budget = Budget(envelopes=[food, gas])

        budget.reset_budget()

        self.assertEqual(50, food.get_current_limit())
        self.assertEqual(30, gas.get_current_limit())
        self.assertEqual([], food.get_expenses())


class EnvelopeTest(unittest.TestCase):
    """Test Envelope model behavior."""

    def test_envelope_generates_id_and_accepts_existing_id(self):
        envelope = Envelope("Food", 50)
        loaded_envelope = Envelope("Food", 50, id="env-1")

        self.assertTrue(envelope.get_id())
        self.assertEqual("env-1", loaded_envelope.get_id())

    def test_envelope_uses_current_limit_when_provided(self):
        envelope = Envelope("Food", 50, current_limit=35)

        self.assertEqual(50, envelope.get_monthly_limit())
        self.assertEqual(35, envelope.get_current_limit())

    def test_envelope_tracks_limits_and_remaining_money(self):
        envelope = Envelope("Food", 50)

        envelope.increase_current_limit(10)
        envelope.decrease_current_limit(5)
        envelope.record_expense(Expense("Groceries", 20, envelope_id=envelope.get_id()))

        self.assertEqual(55, envelope.get_current_limit())
        self.assertEqual(20, envelope.get_total_spent())
        self.assertEqual(35, envelope.get_remaining())
        self.assertEqual(37, envelope.get_percent())

    def test_envelope_percent_returns_zero_when_current_limit_is_zero(self):
        envelope = Envelope("Free", 0)

        self.assertEqual(0, envelope.get_percent())

    def test_envelope_expense_lookup(self):
        envelope = Envelope("Food", 50)
        expense = Expense("Groceries", 20, envelope_id=envelope.get_id())
        envelope.record_expense(expense)

        self.assertIs(expense, envelope.get_expense_by_id(expense.get_id()))
        self.assertIsNone(envelope.get_expense_by_id("missing-id"))

    def test_envelope_rejects_non_positive_expense(self):
        envelope = Envelope("Food", 50)

        envelope.record_expense(Expense("Free sample", 0, envelope_id=envelope.get_id()))

        self.assertEqual([], envelope.get_expenses())

    def test_envelope_reset_restores_current_limit_and_clears_expenses(self):
        envelope = Envelope("Food", 50)
        envelope.decrease_current_limit(10)
        envelope.record_expense(Expense("Groceries", 20, envelope_id=envelope.get_id()))

        envelope.reset_envelope()

        self.assertEqual(50, envelope.get_current_limit())
        self.assertEqual([], envelope.get_expenses())

    def test_envelope_string_contains_summary_values(self):
        envelope = Envelope("Food", 50)
        envelope.record_expense(Expense("Groceries", 25, envelope_id=envelope.get_id()))

        self.assertEqual("Food: $25.0 / $50 -> 50% used", str(envelope))


class ExpenseTest(unittest.TestCase):
    """Test Expense model behavior."""

    def test_expense_generates_id_and_accepts_existing_id(self):
        expense = Expense("Coffee", 5)
        loaded_expense = Expense("Coffee", 5, id="expense-1")

        self.assertTrue(expense.get_id())
        self.assertEqual("expense-1", loaded_expense.get_id())

    def test_expense_tracks_fields(self):
        expense = Expense("Coffee", 5, envelope_id="env-1")

        expense.set_description("Lunch")
        expense.set_amount(12)
        expense.set_envelope("env-2")
        expense.set_date("2026-07-30")

        self.assertEqual("Lunch", expense.get_description())
        self.assertEqual(12, expense.get_amount())
        self.assertEqual("env-2", expense.get_envelope_id())
        self.assertEqual("2026-07-30", expense.get_date())

    def test_expense_rejects_non_positive_amount_update(self):
        expense = Expense("Coffee", 5)

        expense.set_amount(0)
        expense.set_amount(-1)

        self.assertEqual(5, expense.get_amount())

    def test_expense_string_contains_description_and_amount(self):
        expense = Expense("Coffee", 5)

        self.assertEqual("Coffee - $5", str(expense))

    def test_expense_string_includes_date_when_present(self):
        expense = Expense("Coffee", 5, "2026-08-01")

        self.assertEqual("2026-08-01 - Coffee - $5", str(expense))


if __name__ == "__main__":
    unittest.main()
