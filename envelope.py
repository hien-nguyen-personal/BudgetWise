
class Envelope: 
    def __init__(self, name, limit): 
        self.__name: str = name
        self.__limit: float = limit
        self.__expenses: list = []

    def set_name(self, name: str): 
        if len(name) > 0:
            self.__name = name

    def get_name(self) -> str: 
        return self.__name
    
    def set_limit(self, limit: float): 
        if limit > 0:
            self.__limit = limit 

    def get_limit(self) -> float: 
        return self.__limit
    
    def increase_limit(self, amount: float): 
        self.__limit += amount 

    def decrease_limit(self, amount: float): 
        self.__limit -= amount

    def get_balance(self) -> float: 
        balance = 0.0 
        for expense in self.__expenses: 
            balance += expense.get_amount()
        return balance
    
    def get_remaining(self) -> float: 
        return self.__limit - self.get_balance()
    
    def get_percent(self) -> float: 
        return self.get_balance() / self.__limit * 100
    
    def set_expenses(self, expenses: list): 
        self.__expenses = expenses 

    def get_expenses(self) -> list: 
        return self.__expenses
    
    def record_expense(self, expense): 
        if expense.get_amount() > 0:
            self.__expenses.append(expense)
        
    def __eq__(self, other): 
        return isinstance(other, Envelope) and (self.__name == other.get_name()) \
            and (self.__limit == other.get_limit())
    
    def __str__(self): 
        return self.__name + ": " + f"${self.get_balance()} / {self.__limit}" 