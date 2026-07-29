from datetime import date
from uuid import uuid4

class Expense: 
    def __init__(self, description, amount, expense_date=None, envelope_id=None, id=None): 
        self.__id: str = id or str(uuid4())
        self.__description: str = description 
        self.__amount: float = amount 
        self.__envelope_id: str = envelope_id
        self.__date: date = expense_date

    def get_id(self) -> str:
        return self.__id

    def set_description(self, description): 
        self.__description = description

    def get_description(self): 
        return self.__description
    
    def set_amount(self, amount): 
        if amount > 0: 
            self.__amount = amount 

    def get_amount(self): 
        return self.__amount
    
    def set_envelope(self, envelope_id): 
        self.__envelope_id = envelope_id

    def get_envelope_id(self): 
        return self.__envelope_id
    
    def set_date(self, date): 
        self.__date = date 

    def get_date(self): 
        return self.__date
    
    def __str__(self): 
        return f"{self.__description} - ${self.__amount}"
    

    
