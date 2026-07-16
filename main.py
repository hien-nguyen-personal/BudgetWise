
from budget import Budget
from budget_service import BudgetService
from datetime import datetime

def main(): 
    budget = Budget()
    budget_service = BudgetService(budget)

    display_menu()
    user_input = int(input("Enter your choice: ").strip())
    while user_input != 8: 
        if user_input == 1: 
            add_money(budget_service)
        elif user_input == 2: 
            create_envelope(budget_service)
        elif user_input == 3: 
            record_expense(budget_service)
        elif user_input == 4: 
            move_money(budget_service)
        elif user_input == 5: 
            show_budget_summary(budget_service)
        elif user_input == 6: 
            list_expenses(budget_service)
        elif user_input == 7: 
            reset_month(budget_service)
        elif user_input != 8: 
            print("Invalid input. Try again")

        display_menu() 
        user_input = int(input("Enter your choice: ").strip())
        print("")

def display_menu(): 
    print("")
    print("1. Add money")
    print("2. Create envelope")
    print("3. Record expense")
    print("4. Move money")
    print("5. Show budget summary")
    print("6. List expenses")
    print("7. Reset budget")
    print("8. Quit")

def add_money(budget_service: BudgetService): 
    amount = float(input("Amount: ").strip())
    budget_service.add_money(amount)

def create_envelope(budget_service: BudgetService): 
    name = input("Name: ").strip()
    limit = float(input("Limit: ").strip())
    budget_service.create_envelope(name, limit)

def record_expense(budget_service: BudgetService): 
    description = input("Description: ").strip()
    amount = float(input("Amount: ").strip())
    envelope_name = choose_envelope(budget_service)
    budget_service.record_expense(description, amount, envelope_name)

def choose_envelope(budget_service: BudgetService) -> str: 
    envelopes = budget_service.get_budget().get_envelopes()

    for i in range(len(envelopes)): 
        print(f"{i+1}. {envelopes[i].get_name()}")

    selected = int(input("Choose an envelope: ").strip())
    selected_name = envelopes[selected - 1].get_name() 
    return selected_name

def move_money(budget_service: BudgetService): 
    print(budget_service.get_available_money_from_envelopes())
    envelopes = budget_service.get_budget().get_envelopes()

    from_envelope = int(input("From envelope: ").strip())
    to_envelope = int(input("To envelope: ").strip())

    from_envelope_name = envelopes[from_envelope - 1].get_name()
    to_envelope_name = envelopes[to_envelope - 1].get_name()

    amount = float(input("Amount: ").strip())
    budget_service.move_money(from_envelope_name, to_envelope_name, amount)

def show_budget_summary(budget_service: BudgetService): 
    print(budget_service.get_summary())

def list_expenses(budget_service: BudgetService): 
    print("Choose an envelope:")

    envelope_name = choose_envelope(budget_service)
    envelope = budget_service.find_envelope(envelope_name)
    expenses = envelope.get_expenses()

    print()
    for expense in expenses: 
        print(expense)
        print()

def reset_month(budget_service: BudgetService): 
    budget_service.reset_budget()

def read_int(prompt): 
    while True: 
        user_input = input(prompt).strip() 

        try: 
            return int(user_input)      
        except ValueError: 
            print("Please enter a valid number.")

def read_float(prompt): 
    while True: 
        user_input = input(prompt).strip() 

        try: 
            return float(user_input)
        except ValueError: 
            print("Please enter a valid float.")

if __name__ == "__main__": 
    main()
    