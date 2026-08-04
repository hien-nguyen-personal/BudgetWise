import io
import unittest
from unittest.mock import patch

from main import choose_envelope_id, read_date, read_float, read_int, read_text, reset_month
from models.budget import Budget
from services.budget_service import BudgetService


class CliHelperTest(unittest.TestCase):
    """Test reusable CLI input helpers."""

    def test_read_text_reprompts_until_value_is_not_blank(self):
        with patch("builtins.input", side_effect=["", "   ", "Food"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                result = read_text("Name: ")

        self.assertEqual("Food", result)

    def test_read_int_accepts_integer_without_range(self):
        with patch("builtins.input", return_value="42"):
            result = read_int("Number: ")

        self.assertEqual(42, result)

    def test_read_int_reprompts_until_value_is_in_range(self):
        with patch("builtins.input", side_effect=["abc", "0", "11", "5"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                result = read_int("Choose: ", 1, 10)

        self.assertEqual(5, result)

    def test_read_int_supports_min_only(self):
        with patch("builtins.input", side_effect=["2", "3"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                result = read_int("Choose: ", min_value=3)

        self.assertEqual(3, result)

    def test_read_int_supports_max_only(self):
        with patch("builtins.input", side_effect=["11", "10"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                result = read_int("Choose: ", max_value=10)

        self.assertEqual(10, result)

    def test_read_float_reprompts_until_value_is_positive_and_finite(self):
        with patch("builtins.input", side_effect=["abc", "inf", "nan", "0", "-1", "2.5"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                result = read_float("Amount: ")

        self.assertEqual(2.5, result)

    def test_read_date_accepts_iso_date(self):
        with patch("builtins.input", return_value="2026-08-01"):
            result = read_date("Date: ")

        self.assertEqual("2026-08-01", result)

    def test_read_date_reprompts_until_value_is_iso_date(self):
        with patch("builtins.input", side_effect=["August 1", "2026-02-30", "2026-08-01"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                result = read_date("Date: ")

        self.assertEqual("2026-08-01", result)

    def test_choose_envelope_id_returns_selected_envelope_id(self):
        budget = Budget()
        service = BudgetService(budget)
        service.add_money(100)
        service.create_envelope("Food", 50)
        service.create_envelope("Gas", 25)
        gas = budget.get_envelopes()[1]

        with patch("builtins.input", return_value="2"):
            with patch("sys.stdout", new_callable=io.StringIO):
                result = choose_envelope_id(service)

        self.assertEqual(gas.get_id(), result)

    def test_choose_envelope_id_returns_none_when_no_envelopes_exist(self):
        service = BudgetService(Budget())

        with patch("sys.stdout", new_callable=io.StringIO):
            result = choose_envelope_id(service)

        self.assertIsNone(result)

    def test_reset_month_returns_false_when_user_cancels(self):
        budget = Budget()
        service = BudgetService(budget)

        with patch("builtins.input", return_value="n"):
            with patch("sys.stdout", new_callable=io.StringIO):
                result = reset_month(service)

        self.assertFalse(result)

    def test_reset_month_reprompts_and_resets_when_user_confirms(self):
        budget = Budget()
        service = BudgetService(budget)
        service.add_money(100)
        service.create_envelope("Food", 50)
        envelope = budget.get_envelopes()[0]
        service.record_expense("Coffee", 5, envelope.get_id())

        with patch("builtins.input", side_effect=["maybe", "y"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                result = reset_month(service)

        self.assertTrue(result)
        self.assertEqual([], envelope.get_expenses())


if __name__ == "__main__":
    unittest.main()
