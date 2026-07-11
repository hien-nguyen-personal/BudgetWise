from envelope import Envelope
from datetime import date

class Expense: 
    def __init__(self, description, amount, envelope, expense_date): 
        self.__description: str = description 
        self.__amount: float = amount 
        self.__envelope: Envelope = envelope
        self.__date: date = expense_date

    def set_description(self, description): 
        self.__description = description

    def get_description(self): 
        return self.__description
    
    def set_amount(self, amount): 
        if amount > 0: 
            self.__amount = amount 

    def get_amount(self): 
        return self.__amount
    
    def set_envelope(self, envelope): 
        self.__envelope = envelope

    def get_envelope(self): 
        return self.__envelope 
    
    def set_date(self, date): 
        self.__date = date 

    def get_date(self): 
        return self.__date
    
    def __str__(self): 
        return self.__description + "\n" + f"Amount: ${self.__amount}" + "\n" + self.__envelope 
    

    