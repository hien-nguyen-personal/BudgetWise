class Expense: 
    def __init__(self, description, amount, category, date): 
        self.description = description 
        self.amount = amount 
        self.category = category 
        self.date = date 

    def set_description(self, description): 
        self.description = description

    def get_description(self): 
        return self.description
    
    def set_amount(self, amount): 
        self.amount = amount 

    def get_amount(self): 
        return self.amount
    
    def set_category(self, category): 
        self.category = category

    def get_category(self): 
        return self.category 
    
    def set_date(self, date): 
        self.date = date 

    def get_date(self): 
        return self.date
    
    def __str__(self): 
        return self.description + "\n" + f"Amount: ${self.amount}" + "\n" + self.category 
    

    