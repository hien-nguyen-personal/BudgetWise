from uuid import uuid4
import math

class Envelope: 
    def __init__(self, name, monthly_limit, id=None, current_limit=None, expenses=None): 
        self.__id: str = id or str(uuid4())
        self.__name: str = name
        self.__monthly_limit: float = monthly_limit
        self.__current_limit: float = current_limit if current_limit is not None else monthly_limit
        self.__expenses: list = expenses or []


    def set_name(self, name: str): 
        if len(name) > 0:
            self.__name = name

    def get_name(self) -> str: 
        return self.__name
    
    def set_monthly_limit(self, monthly_limit: float): 
        self.__monthly_limit = monthly_limit 

    def get_monthly_limit(self) -> float: 
        return self.__monthly_limit

    def set_current_limit(self, current_limit: float): 
        self.__current_limit = current_limit 

    def get_current_limit(self) -> float: 
        return self.__current_limit
    
    def increase_current_limit(self, amount: float): 
        self.__current_limit += amount 

    def decrease_current_limit(self, amount: float): 
        self.__current_limit -= amount

    def get_id(self) -> str: 
        return self.__id

    def get_total_spent(self) -> float: 
        total = 0.0 
        for expense in self.__expenses: 
            total += expense.get_amount()
        return total
    
    def get_remaining(self) -> float: 
        return self.__current_limit - self.get_total_spent()
    
    def get_percent(self) -> float: 
        if self.__current_limit == 0:
            return 0
        return math.ceil(self.get_total_spent() / self.__current_limit * 100)
    
    def set_expenses(self, expenses: list): 
        self.__expenses = expenses 

    def get_expenses(self) -> list: 
        return self.__expenses
    
    def record_expense(self, expense): 
        if expense.get_amount() > 0:
            self.__expenses.append(expense)

    def get_expense_by_id(self, expense_id: str):
        for expense in self.__expenses:
            if expense.get_id() == expense_id:
                return expense
        return None

    def reset_envelope(self): 
        self.__current_limit = self.__monthly_limit
        self.__expenses = []
        
    def __eq__(self, other): 
        return isinstance(other, Envelope) and (self.__name == other.get_name()) \
            and (self.__monthly_limit == other.get_monthly_limit())
    
    def __str__(self): 
        return (
            f"{self.__name}: ${self.get_total_spent()} / " 
            f"${self.__current_limit} -> {self.get_percent()}% used"
            )
