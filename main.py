from expense import Expense

from datetime import datetime

def main(): 
    expense = create_expense()

def create_expense() -> Expense: 
    description = input("Description: ")
    amount = float(input("Amount: "))
    category = input("Category: ")
    date = datetime.now()
    return Expense(description, amount, category, date)



if __name__ == "__main__": 
    main()
    