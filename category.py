class Category: 
    def __init__(self, name, limit, balance, expenses): 
        self.name = name
        self.limit = limit
        self.balance = balance 
        self.expenses = expenses

    def set_name(self, name): 
        self.name = name

    def get_name(self): 
        return self.name
    
    def set_limit(self, limit): 
        self.limit = limit 

    def get_limit(self): 
        return self.limit
    
    def set_balance(self, balance): 
        self.balance = balance 

    def get_balance(self): 
        return self.balance
    
    def reset_balance(self): 
        self.balance = 0
    
    def set_expenses(self, expenses): 
        self.expenses = expenses 

    def get_expenses(self): 
        return self.expenses
    
    def add_expense(self, expense): 
        self.balance += expense.get_amount()
        self.expenses.add(expense)

    def get_total(self): 
        total = 0.0 
        for expense in self.expenses: 
            total += expense.get_amount()
        
        return total 
    
    def get_percent(self): 
        return self.balance / self.limit
        
    def __eq__(self, other): 
        return isinstance(other, Category) and (self.name == other.name) \
            and (self.limit == other.limit)
    
    def __str__(self): 
        return self.name + ": " + f"${self.balance} / {self.limit}" 