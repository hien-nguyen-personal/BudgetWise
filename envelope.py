class Envelope: 
    def __init__(self, name, limit, balance, expenses): 
        self.__name = name
        self.__limit = limit
        self.__balance = balance 
        self.__expenses = expenses

    def set_name(self, name): 
        self.__name = name

    def get_name(self): 
        return self.__name
    
    def set_limit(self, limit): 
        self.__limit = limit 

    def get_limit(self): 
        return self.__limit
    
    def set_balance(self, balance): 
        self.__balance = balance 

    def get_balance(self): 
        return self.__balance
    
    def reset_balance(self): 
        self.__balance = 0
    
    def set_expenses(self, expenses): 
        self.__expenses = expenses 

    def get_expenses(self): 
        return self.__expenses
    
    def add_expense(self, expense): 
        self.__balance += expense.get_amount()
        self.__expenses.add(expense)

    def get_balance(self): 
        return self.__balance
    
    def get_percent(self): 
        return self.__balance / self.__limit
        
    def __eq__(self, other): 
        return isinstance(other, Envelope) and (self.__name == other.get_name) \
            and (self.__limit == other.get_limit)
    
    def __str__(self): 
        return self.__name + ": " + f"${self.__balance} / {self.__limit}" 