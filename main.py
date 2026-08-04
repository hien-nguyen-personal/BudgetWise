"""Command-line interface for the BudgetWise envelope budgeting app."""

from datetime import date
from math import isfinite

from repositories.budget_repository import BudgetRepository
from services.budget_service import BudgetService


def main():
    """Run the main menu loop and save the budget after successful changes."""
    repository = BudgetRepository()
    budget = repository.load_budget()
    budget_service = BudgetService(budget)

    while True:
        display_menu()
        user_input = read_int("Enter your choice: ", 1, 11)
        print("")

        changed = False

        if user_input == 1:
            changed = add_money(budget_service)
        elif user_input == 2:
            changed = create_envelope(budget_service)
        elif user_input == 3:
            changed = record_expense(budget_service)
        elif user_input == 4:
            changed = move_money(budget_service)
        elif user_input == 5:
            show_budget_summary(budget_service)
        elif user_input == 6:
            list_expenses(budget_service)
        elif user_input == 7:
            changed = edit_expense(budget_service)
        elif user_input == 8:
            changed = edit_envelope(budget_service)
        elif user_input == 9:
            changed = reset_month(budget_service)
        elif user_input == 10: 
            changed = delete_envelope(budget_service)
        elif user_input == 11:
            print("Goodbye.")
            break

        if changed:
            repository.save_budget(budget_service.get_budget())


def display_menu():
    """Print the available CLI menu options."""
    print("")
    print("1. Add money")
    print("2. Create envelope")
    print("3. Record expense")
    print("4. Move money")
    print("5. Show budget summary")
    print("6. List expenses")
    print("7. Edit expense")
    print("8. Edit envelope")
    print("9. Reset budget")
    print("10. Delete envelope")
    print("11. Quit")


def add_money(budget_service: BudgetService) -> bool:
    """Prompt for unassigned money and add it to the budget.

    Args:
        budget_service: Service that owns budget workflows.

    Returns:
        True if money was added; otherwise False.
    """
    amount = read_float("Amount: ")

    if budget_service.add_money(amount):
        print(f"Successfully added ${amount}.")
        return True

    print("Please enter an amount greater than 0.")
    return False


def create_envelope(budget_service: BudgetService) -> bool:
    """Prompt for envelope details and create a funded envelope.

    Args:
        budget_service: Service that owns budget workflows.

    Returns:
        True if an envelope was created; otherwise False.
    """
    print(f"Money available: ${budget_service.get_budget().get_money_available()}")

    if not budget_service.has_money_available():
        print("Unable to create envelope. Please add money first.")
        return False

    name = read_text("Name: ")
    limit = read_float("Limit: ")

    if budget_service.create_envelope(name, limit):
        print(f"Successfully created envelope: {name} with limit ${limit}.")
        print(f"You have ${budget_service.get_budget().get_money_available()} available.")
        return True

    print("Unable to create envelope. Check that the name is unique and enough money is available.")
    return False


def record_expense(budget_service: BudgetService) -> bool:
    """Prompt for an expense and record it in the selected envelope.

    Args:
        budget_service: Service that owns budget workflows.

    Returns:
        True if an expense was recorded; otherwise False.
    """
    if not budget_service.contains_envelopes():
        print("Unable to record expense. Please create an envelope first.")
        return False

    envelope_id = choose_envelope_id(budget_service, "Choose an envelope for the expense: ")

    if not envelope_id:
        print("Unable to find envelope.")
        return False

    description = read_text("Description: ")
    amount = read_float("Amount: ")
    expense_date = read_date("Date (YYYY-MM-DD): ")

    if budget_service.record_expense(description, amount, envelope_id, expense_date):
        print("Expense recorded.")
        return True

    print("Unable to record expense. Check the description, amount, and envelope remaining.")
    return False


def choose_envelope_id(budget_service: BudgetService, prompt="Choose an envelope: "):
    """Print envelopes and return the ID for the selected envelope.

    Args:
        budget_service: Service used to access the current budget.
        prompt: Input prompt shown when asking for the envelope choice.

    Returns:
        The selected envelope ID, or None if no envelopes exist.
    """
    envelopes = budget_service.get_budget().get_envelopes()

    if not envelopes:
        print("There are currently no envelopes. Please create an envelope.")
        return None

    for index, envelope in enumerate(envelopes):
        print(f"{index + 1}. {envelope.get_name()}")

    selected = read_int(prompt, 1, len(envelopes))
    return envelopes[selected - 1].get_id()


def move_money(budget_service: BudgetService) -> bool:
    """Prompt for two envelopes and move money between them.

    Args:
        budget_service: Service that owns budget workflows.

    Returns:
        True if money was moved; otherwise False.
    """
    envelopes = budget_service.get_budget().get_envelopes()

    if len(envelopes) < 2:
        print("Unable to move money. Please create at least two envelopes first.")
        return False

    print(budget_service.get_available_money_from_envelopes())

    from_envelope_index = read_int("From envelope: ", 1, len(envelopes))
    to_envelope_index = read_int("To envelope: ", 1, len(envelopes))

    from_envelope = envelopes[from_envelope_index - 1]
    to_envelope = envelopes[to_envelope_index - 1]

    if from_envelope.get_id() == to_envelope.get_id():
        print("Unable to move money. Choose two different envelopes.")
        return False

    amount = read_float("Amount: ")

    if budget_service.move_money(from_envelope.get_id(), to_envelope.get_id(), amount):
        print(f"Successfully moved ${amount} from {from_envelope.get_name()} to {to_envelope.get_name()}.")
        return True

    print("Unable to move money. Check that the source envelope has enough remaining.")
    return False


def show_budget_summary(budget_service: BudgetService):
    """Print the current budget summary.

    Args:
        budget_service: Service used to build the summary.
    """
    print(budget_service.get_summary())


def list_expenses(budget_service: BudgetService):
    """Print expenses for a selected envelope.

    Args:
        budget_service: Service used to access envelopes and expenses.
    """
    if not budget_service.contains_envelopes():
        print("Unable to list expenses. Please add an envelope first.")
        return

    envelope_id = choose_envelope_id(budget_service)

    if not envelope_id:
        print("Unable to find envelope.")
        return

    envelope = budget_service.find_envelope_by_id(envelope_id)
    expenses = envelope.get_expenses()

    if not expenses:
        print("No expenses recorded.")
        return

    print("")
    for expense in expenses:
        print(expense)
        print("")


def edit_expense(budget_service: BudgetService) -> bool:
    """Prompt for an expense and update its description and amount.

    Args:
        budget_service: Service that owns budget workflows.

    Returns:
        True if an expense was updated; otherwise False.
    """
    if not budget_service.contains_envelopes():
        print("Unable to edit expense. Please create an envelope first.")
        return False

    envelope_id = choose_envelope_id(budget_service, "Choose an envelope with the expense: ")

    if not envelope_id:
        print("Unable to find envelope.")
        return False

    envelope = budget_service.find_envelope_by_id(envelope_id)
    expenses = envelope.get_expenses()

    if not expenses:
        print("No expenses recorded for this envelope.")
        return False

    for index, expense in enumerate(expenses):
        print(f"{index + 1}. {expense}")

    selected = read_int("Choose an expense: ", 1, len(expenses))
    expense = expenses[selected - 1]

    description = read_text("New description: ")
    amount = read_float("New amount: ")

    if budget_service.edit_expense(expense.get_id(), description, amount):
        print("Expense updated.")
        return True

    print("Unable to update expense. Check the description, amount, and envelope remaining.")
    return False


def edit_envelope(budget_service: BudgetService) -> bool:
    """Prompt for an envelope and update its name.

    Args:
        budget_service: Service that owns budget workflows.

    Returns:
        True if an envelope was updated; otherwise False.
    """
    if not budget_service.contains_envelopes():
        print("Unable to edit envelope. Please create an envelope first.")
        return False

    envelope_id = choose_envelope_id(budget_service)

    if not envelope_id:
        print("Unable to find envelope.")
        return False

    name = read_text("New name: ")

    if budget_service.edit_envelope(envelope_id, name):
        print("Envelope updated.")
        return True

    print("Unable to update envelope. Check that the name is not blank or already used.")
    return False

def delete_envelope(budget_service: BudgetService) -> bool: 
    """Prompt for an envelope and delete it. 

    Args:
        budget_service: Service that owns budget workflows. 

    Returns: 
        True if an envelope was update; otherewise False. 
    """

    if not budget_service.contains_envelopes(): 
        print("Unable to delete envelope. Please create an envelope first.")
        return False
    
    envelope_id = choose_envelope_id(budget_service)

    if not envelope_id: 
        print("Unable to find envelope.")
        return False 
    
    if budget_service.delete_envelope(envelope_id): 
        print("Envelope deleted.")
        return True 
    
    print("Unable to delete envelope.")
    return False



def reset_month(budget_service: BudgetService) -> bool:
    """Confirm and reset all envelopes for a new month.

    Args:
        budget_service: Service that owns budget workflows.

    Returns:
        True if the budget was reset; otherwise False.
    """
    while True:
        user_input = input("Are you sure you want to reset this month's budget? (Y/N) ").strip().lower()

        if user_input == "y":
            budget_service.reset_budget()
            print("Budget reset.")
            return True

        if user_input == "n":
            print("Canceling reset month operation.")
            return False

        print("Please enter Y or N.")


def read_text(prompt):
    """Read non-blank text from the user.

    Args:
        prompt: Prompt shown before reading input.

    Returns:
        A stripped, non-empty string.
    """
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Please enter a value.")


def read_int(prompt, min_value=None, max_value=None):
    """Read an integer from the user with optional range limits.

    Args:
        prompt: Prompt shown before reading input.
        min_value: Optional lowest allowed value.
        max_value: Optional highest allowed value.

    Returns:
        A valid integer.
    """
    while True:
        user_input = input(prompt).strip()

        try:
            value = int(user_input)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if min_value is not None and value < min_value:
            print(f"Please enter at least {min_value}.")
            continue

        if max_value is not None and value > max_value:
            print(f"Please enter no more than {max_value}.")
            continue

        return value


def read_float(prompt):
    """Read a positive finite float from the user.

    Args:
        prompt: Prompt shown before reading input.

    Returns:
        A float greater than zero.
    """
    while True:
        user_input = input(prompt).strip()

        try:
            value = float(user_input)
        except ValueError:
            print("Please enter a valid amount.")
            continue

        if not isfinite(value):
            print("Please enter a valid amount.")
            continue

        if value <= 0:
            print("Please enter an amount greater than 0.")
            continue

        return value


def read_date(prompt):
    """Read a valid ISO date from the user.

    Args:
        prompt: Prompt shown before reading input.

    Returns:
        A date string in YYYY-MM-DD format.
    """
    while True:
        user_input = input(prompt).strip()

        if len(user_input) != 10 or user_input[4] != "-" or user_input[7] != "-":
            print("Please enter a date in YYYY-MM-DD format.")
            continue

        year, month, day = user_input.split("-")
        if not year.isdigit() or not month.isdigit() or not day.isdigit():
            print("Please enter a date in YYYY-MM-DD format.")
            continue

        try:
            expense_date = date.fromisoformat(user_input)
        except ValueError:
            print("Please enter a date in YYYY-MM-DD format.")
            continue

        return expense_date.isoformat()


if __name__ == "__main__":
    main()
