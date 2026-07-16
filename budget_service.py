from budget import Budget
from expense import Expense
from envelope import Envelope

class BudgetService: 

    def __init__(self, budget: Budget): 
        self.__budget = budget

    def get_budget(self) -> Budget: 
        return self.__budget

    def set_budget(self, budget: Budget): 
        self.__budget = budget

    def create_envelope(self, name: str, limit: float) -> bool: 
        if self.is_positive_amount(limit) and limit <= self.__budget.get_money_available():
            if not self.find_envelope(name) and len(name) > 0: 
                envelope = Envelope(name, limit)
                self.__budget.add_envelope(envelope)
                self.__budget.decrease_money_available(limit)
                return True
        return False
    
    def _is_valid_limit(self, limit) -> bool: 
        return limit <= self.__budget.get_money_available()

    def add_money(self, money: float) -> bool: 
        if self._is_positive_amount(money): 
            self.__budget.add_money(money)
            return True
        return False

    def record_expense(self, description: str, amount: float, envelope_name: str) -> bool:
        envelope = self.find_envelope(envelope_name)
        if len(description) > 0 and self._is_positive_amount(amount) and envelope: 
            expense = Expense(description, amount, envelope, None)
            envelope.record_expense(expense)
            return True 
        return False
    
    def _is_positive_amount(self, amount) -> bool: 
        return amount > 0

    
    def find_envelope(self, envelope_name: str) -> Envelope: 
        return self.__budget.get_envelope_by_name(envelope_name)
    
    def move_money(self, from_envelope_name: str, to_envelope_name: str, amount: float) -> bool: 
        if amount > 0: 
            from_envelope = self.find_envelope(from_envelope_name)
            to_envelope = self.find_envelope(to_envelope_name)

            if from_envelope and to_envelope: 
                if from_envelope.get_remaining() > amount: 
                    to_envelope.increase_current_limit(amount)
                    from_envelope.decrease_current_limit(amount)
                    return True

        return False
    
    def get_available_money_from_envelopes(self) -> str: 
        result = "Available money per envelope: \n"
        envelopes = self.__budget.get_envelopes()
        for index, envelope in enumerate(envelopes): 
            result += f"{index+1}. {envelope.get_name()}: ${envelope.get_remaining()} \n"
        return result
    
    def reset_budget(self): 
        self.__budget.reset_budget()
    
    def get_summary(self): 
        return "Budget: \n" + f"{self.__budget}"