class ExpenseService: 

    def __init__(self): 
        self.__expenses = []

    def add_expense(self, expense): 
        self.__expenses.append(expense)
    
    def get_expenses(self): 
        return self.__expenses.copy()
    
    def get_expense_by_id(self, expense_id): 
        for expense in self.__expenses: 
            if expense.get_id() == expense_id(): 
                return expense
    
    def edit_expense(self, expense_id, new_expense): 
        for expense in self.__expenses: 
            if expense.get_id() == expense_id: 
                expense.set_amount(new_expense.get_amount())
                expense.set_store(new_expense.get_store())
                expense.set_category(new_expense.get_category())
                expense.set_date(new_expense.get_date())
                expense.set_description(new_expense.get_description())
                expense.set_payment_method(new_expense.get_payment_method())
                return True
        return False
    
    def delete_expense(self, expense_id): 
        for expense in self.__expenses: 
            if expense.get_id() == expense_id: 
                self.__expenses.remove(expense)
                return True 
        return False
    
    def get_total_expenses(self): 
        total = 0 
        for expense in self.__get_expenses(): 
            total += expense.get_amount()

        return total
    
    def get_expenses_by_category(self, category): 
        expenses_by_category = []
        for expense in self.__expenses: 
            if expense.get_category() == category: 
                expenses_by_category.append(expense) 
        return expenses_by_category
    
    def list_expenses_by_category(self, category): 
        expenses_by_category = self.get_expenses_by_category(category)
        for expense in expenses_by_category: 
            print(expense)
    
    
    

