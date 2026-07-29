from models.budget import Budget
from models.expense import Expense
from models.envelope import Envelope

class BudgetService: 

    def __init__(self, budget: Budget): 
        self.__budget = budget

    def get_budget(self) -> Budget: 
        return self.__budget

    def set_budget(self, budget: Budget): 
        self.__budget = budget

    def create_envelope(self, name: str, limit: float) -> bool: 
        name = name.strip()

        if not self._is_valid_name(name):
            return False

        if not self._is_unique_envelope_name(name):
            return False

        if not self._is_positive_amount(limit):
            return False

        if not self._has_enough_available_money(limit):
            return False

        envelope = Envelope(name, limit)
        self.__budget.add_envelope(envelope)
        self.__budget.decrease_money_available(limit)
        return True

    def edit_envelope(self, envelope_id: str, name: str) -> bool:
        envelope = self.find_envelope_by_id(envelope_id)
        name = name.strip()

        if not envelope:
            return False

        if not self._is_valid_name(name):
            return False

        if not self._is_unique_envelope_name(name, envelope_id):
            return False

        envelope.set_name(name)
        return True

    def edit_expense(self, expense_id: str, description: str, amount: float) -> bool:
        result = self._find_expense_and_envelope(expense_id)

        if not result:
            return False

        envelope, expense = result
        description = description.strip()

        if not self._is_valid_name(description):
            return False

        if not self._is_positive_amount(amount):
            return False

        available_after_removing_current_expense = envelope.get_remaining() + expense.get_amount()
        if available_after_removing_current_expense < amount:
            return False

        expense.set_description(description)
        expense.set_amount(amount)
        return True

    def _has_enough_available_money(self, amount) -> bool:
        return amount <= self.__budget.get_money_available()

    def _is_unique_envelope_name(self, name: str, current_envelope_id=None) -> bool:
        for envelope in self.__budget.get_envelopes():
            if envelope.get_id() == current_envelope_id:
                continue

            if envelope.get_name().lower() == name.lower():
                return False

        return True

    def _is_valid_name(self, name: str) -> bool:
        return len(name.strip()) > 0

    def _find_expense_and_envelope(self, expense_id: str):
        for envelope in self.__budget.get_envelopes():
            expense = envelope.get_expense_by_id(expense_id)
            if expense:
                return envelope, expense

        return False
    
    def has_money_available(self) -> bool: 
        return self._is_positive_amount(self.__budget.get_money_available())
    
    def _is_valid_limit(self, limit) -> bool: 
        return self._is_positive_amount(limit) and self._has_enough_available_money(limit)

    def add_money(self, money: float) -> bool: 
        if self._is_positive_amount(money): 
            self.__budget.add_money(money)
            return True
        return False

    def record_expense(self, description: str, amount: float, envelope_id: str) -> bool:
        envelope = self.find_envelope_by_id(envelope_id)
        description = description.strip()

        if not envelope:
            return False

        if not self._is_valid_name(description):
            return False

        if not self._is_positive_amount(amount):
            return False

        if envelope.get_remaining() < amount:
            return False

        expense = Expense(description, amount, None, envelope.get_id())
        envelope.record_expense(expense)
        return True
    
    def _is_positive_amount(self, amount) -> bool: 
        return amount is not None and amount > 0

    
    def find_envelope(self, envelope_name: str) -> Envelope: 
        return self.__budget.get_envelope_by_name(envelope_name)

    def find_envelope_by_id(self, envelope_id: str) -> Envelope:
        return self.__budget.get_envelope_by_id(envelope_id)
    
    def contains_envelopes(self) -> bool: 
        return len(self.__budget.get_envelopes()) > 0
    
    def move_money(self, from_envelope_id: str, to_envelope_id: str, amount: float) -> bool: 
        if from_envelope_id == to_envelope_id:
            return False

        if not self._is_positive_amount(amount):
            return False

        from_envelope = self.find_envelope_by_id(from_envelope_id)
        to_envelope = self.find_envelope_by_id(to_envelope_id)

        if not from_envelope or not to_envelope:
            return False

        if from_envelope.get_remaining() < amount:
            return False

        to_envelope.increase_current_limit(amount)
        from_envelope.decrease_current_limit(amount)
        return True
    
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
