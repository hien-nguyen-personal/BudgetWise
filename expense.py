class Expense: 



    def __init__(self, amount, store, category, date):
        self.amount = amount
        self.store = store
        self.category = category
        self.date = date
        self.id = None 
        self.user_id = None 

    def set_amount(self, amount): 
        self.amount = amount

    def get_amount(self): 
        return self.amount 
    
    def set_store(self, store): 
        self.store = store 
    
    def get_store(self): 
        return self.store

    def set_category(self, category): 
        self.category = category 
    
    def get_category(self): 
        return self.category 
    
    def set_date(self, date): 
        self.date = date 
    
    def get_date(self): 
        return self.date

    def set_id(self, id): 
        self.id = id 
    
    def set_user_id(self, user_id): 
        self.user_id = user_id
        
    def __str__(self):
        return f"Expense(amount={self.amount}, category='{self.category}', date='{self.date}')"