class Budget: 
    def __init__(self): 
        self.__envelopes = []
        self.__moneyAvailable = 0 

    def set_envelopes(self, envelopes): 
        self.__envelopes = envelopes 

    def get_envelopes(self): 
        return self.__envelopes 
    
    def add_envelope(self, envelope, amount): 
        self.__envelopes.append(envelope)
        self.__moneyAvailable -= amount

    def addMoney(self, amount): 
        self.__moneyAvailable += amount

    def record_expense(self, envelope, expense): 


    def get_total(self): 
        total = 0.0
        for envelope in self.envelopes: 
            total += envelope.get_total()
        
        return total