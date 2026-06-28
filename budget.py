class Budget: 

    def __init__(self, category, limit, balance): 
        self.category = category
        self.limit = limit
        self.balance = balance 
        self.id = None
        self.user_id = None

    def set_category(self, category): 
        self.category = category 

    def get_category(self): 
        return self.category 
    
    def set_limit(self, limit): 
        self.limit = limit 

    def get_limit(self): 
        return self.limit 
    
    def set_balance(self, balance): 
        self.balance = balance 
    
    def get_balance(self): 
        return self.balance 
    
    def set_id(self, id): 
        self.id = id 

    def set_user_id(self, user_id): 
        self.user_id = user_id 

    def __str__(self): 
        return f"Budget(category='{self.category}', limit={self.limit}, balance={self.balance})"