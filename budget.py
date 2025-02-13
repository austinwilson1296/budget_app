import json
'''
This class will be used to create budgets
'''

class Budget:
    def __init__(self, month: str, categories: dict[str,float]):
        
        self.month = month
        self.categories = categories
        

        

    def __str__(self):
        return f"{self.month} | {self.categories}"
    
    def add_category(self,category: str, amount: float):
        self.categories[category] = amount

    def remove_category(self,category: str):
        del self.categories[category]
    
    def update_category(self,category: str, amount: float):
        self.categories[category] = amount

  

    
    
