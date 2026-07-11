from envelope import Envelope

class Budget: 
    def __init__(self): 
        self.__envelopes: list[Envelope] = []
        self.__money_available: float = 0 

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
    
    def get_money_available(self) -> float: 
        return self.__money_available
    
    def set_money_available(self, money_available: float): 
        self.__money_available = money_available

    def add_money(self, money: float): 
        self.__money_available += money

    def get_total_spent(self) -> float: 
        total = 0.0
        for envelope in self.__envelopes: 
            total += envelope.get_balance()
        
        return total

