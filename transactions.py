import datetime
import categories as cat
'''
Transaction class will handle all income and expenses transactions
'''

class Transaction:
    def __init__(self, tran_type: str, amount: float, date: str,category: str, description: str):
        self.tran_type = self.validate_tran_type(tran_type)
        self.amount = self.validate_amount(float(amount))
        self.date = self.validate_date(date)
        self.category = category
        self.description = description

    

    def __str__(self):
        return f"{self.date} | {self.amount} | {self.description}"
    
    def validate_amount(self,amount):

        try:
            return float(amount)
        except ValueError:
            raise ValueError("Amount must be a number")
        
    def validate_date(self,date):
        try:
            return datetime.datetime.strptime(date, "%m-%d-%y")
        except ValueError:
            raise ValueError("Date must be in the format MM-DD-YY")
        
    def validate_tran_type(self,tran_type):
        if tran_type not in ["Income","Expense"]:
            raise ValueError("Transaction type must be either Income or Expense")
        return tran_type
    
    def validate_category(self,category):
        if category not in cat.BUDGET_CATEGORIES:
            raise ValueError("Category must be in the list of budget categories")
        return category
        
 
        