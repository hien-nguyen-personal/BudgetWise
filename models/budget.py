from models.envelope import Envelope
from uuid import uuid4

class Budget: 
    def __init__(self, id=None, money_available=0, envelopes=None): 
        self.__id: str = id or str(uuid4())
        self.__envelopes: list[Envelope] = envelopes or []
        self.__money_available: float = money_available

    def get_id(self) -> str:
        return self.__id

    def set_envelopes(self, envelopes: list[Envelope]): 
        self.__envelopes = envelopes 

    def get_envelopes(self) -> list[Envelope]: 
        return self.__envelopes 
    
    def add_envelope(self, envelope: Envelope): 
        self.__envelopes.append(envelope)

    def get_envelope_by_name(self, envelope_name: str) -> Envelope: 
        for envelope in self.__envelopes: 
            if envelope.get_name() == envelope_name:
                return envelope 
        return None
    
    def get_envelope_by_id(self, envelope_id: str) -> Envelope: 
        for envelope in self.__envelopes: 
            if envelope.get_id() == envelope_id: 
                return envelope
        return None
    
    def get_money_available(self) -> float: 
        return self.__money_available
    
    def set_money_available(self, money_available: float): 
        self.__money_available = money_available

    def decrease_money_available(self, amount: float): 
        self.__money_available -= amount 

    def increase_money_available(self, amount: float): 
        self.__money_available += amount

    def add_money(self, money: float): 
        self.__money_available += money

    def get_total_spent(self) -> float: 
        total = 0.0
        for envelope in self.__envelopes: 
            total += envelope.get_total_spent()
        return total
    
    def reset_budget(self): 
        for envelope in self.__envelopes: 
            envelope.reset_envelope()
    
    def __str__(self): 
        result = "Money available: " + f"${self.__money_available} \n" 
        for envelope in self.__envelopes: 
            result += f"{envelope}" + "\n"
        return result

