from budget import Budget
from expense import Expense
from envelope import Envelope

class BudgetService: 

    def __init__(self, budget: Budget): 
        self.__budget = budget

    def get_budget(self): 
        return self.__budget

    def set_budget(self, budget: Budget): 
        self.__budget = budget

    def create_envelope(self, name: str, limit: float) -> bool: 
        if len(name) > 0 and limit > 0: 
            envelope = Envelope(name, limit)
            self.__budget.add_envelope(envelope)
            return True
        return False

    def add_money(self, money: float) -> bool: 
        if money > 0: 
            self.__budget.add_money(money)
            return True
        return False

    def record_expense(self, description: str, amount: float, envelope_name: str):
        envelope = self.find_envelope(envelope_name)
        if len(description) > 0 and amount > 0 and envelope: 
            expense = Expense(description, amount, envelope, None)
            envelope.record_expense(expense)
            return True 
        return False
    
    def find_envelope(self, envelope_name: str) -> Envelope: 
        return self.__budget.get_envelope_by_name(envelope_name)
    
    def move_money(self, from_envelope_name: str, to_envelope_name: str, amount: float) -> bool: 
        if amount > 0: 
            from_envelope = self.find_envelope(from_envelope_name)
            to_envelope = self.find_envelope(to_envelope_name)

            if from_envelope and to_envelope: 
                if from_envelope.get_remaining() > amount: 
                    to_envelope.increase_limit(amount)
                    from_envelope.decrease_limit(amount)

        return False