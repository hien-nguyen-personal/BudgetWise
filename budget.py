class Budget: 
    def __init__(self, categories): 
        self.categories = categories 

    def set_categories(self, categories): 
        self.categories = categories 

    def get_categories(self): 
        return self.categories 
    
    def add_category(self, category): 
        self.categories.append(category)

    def add_expense(self, expense): 
        for category in self.categories: 
            if category == expense.get_category(): 
                category.add(expense)
                break 

    def get_total(self): 
        total = 0.0
        for category in self.categories: 
            total += category.get_total()
        
        return total