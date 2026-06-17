from datetime import date

from insights import SpendingInsights
from item import Item
from storage import ItemStorage


class BudgetTrackerApp:
    """Command-line interface for the budget tracker."""

    def __init__(self):
        self.storage = ItemStorage()
        self.items = self.storage.load_items()

    def run(self):
        """Keep showing the main menu until the user exits."""
        while True:
            self.show_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.add_item()
            elif choice == "2":
                self.view_items()
            elif choice == "3":
                self.view_insights()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Please enter a number from 1 to 4.")

    def show_menu(self):
        print("\nBudget Tracker\n")
        print("1. Add Item")
        print("2. View Items")
        print("3. View Insights")
        print("4. Exit")

    def add_item(self):
        print("\nAdd Item")

        name = self.prompt_required_text("Item name: ")
        category = self.prompt_required_text("Category: ")
        store = self.prompt_required_text("Store: ")
        quantity = self.prompt_positive_int("Quantity: ")
        price = self.prompt_non_negative_float("Price: ")
        item_date = self.prompt_date("Date (YYYY-MM-DD): ")

        item = Item(
            name=name,
            category=category,
            store=store,
            quantity=quantity,
            price=price,
            date=item_date,
        )
        self.items.append(item)
        self.storage.save_items(self.items)

        print("Item added and saved.")

    def view_items(self):
        print("\nSaved Items")

        if not self.items:
            print("No items saved yet.")
            return

        for index, item in enumerate(self.items, start=1):
            print(f"\nItem {index}")
            print(item.display())

    def view_insights(self):
        print("\nSpending Insights")

        if not self.items:
            print("No spending data available yet.")
            return

        insights = SpendingInsights(self.items)

        print(f"Total Spending: ${insights.total_spending():.2f}")
        self.print_grouped_totals("By Category", insights.spending_by_category())
        self.print_grouped_totals("By Store", insights.spending_by_store())

    def print_grouped_totals(self, title, totals):
        print(f"\n{title}:")

        for name, amount in sorted(totals.items()):
            print(f"{name}: ${amount:.2f}")

    def prompt_required_text(self, prompt):
        while True:
            value = input(prompt).strip()

            if value:
                return value

            print("This field cannot be empty.")

    def prompt_positive_int(self, prompt):
        while True:
            value = input(prompt).strip()

            try:
                number = int(value)
            except ValueError:
                print("Please enter a whole number.")
                continue

            if number > 0:
                return number

            print("Please enter a number greater than 0.")

    def prompt_non_negative_float(self, prompt):
        while True:
            value = input(prompt).strip().replace("$", "")

            try:
                number = float(value)
            except ValueError:
                print("Please enter a valid price.")
                continue

            if number >= 0:
                return number

            print("Please enter a price of 0 or more.")

    def prompt_date(self, prompt):
        while True:
            value = input(prompt).strip()

            try:
                date.fromisoformat(value)
            except ValueError:
                print("Please enter a date in YYYY-MM-DD format.")
                continue

            return value


if __name__ == "__main__":
    app = BudgetTrackerApp()
    app.run()
