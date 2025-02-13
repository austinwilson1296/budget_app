import tkinter as tk
from tkinter import ttk,messagebox
import transactions as tr
from utils import *
import categories as cat
import budget as bg
import json

'''
This is the main class that will hold the main config for the app
Will include all methods and attributes that will be used in the app
'''
class BudgetTrackApp():
    def __init__(self,root):
        def __repr__(self):
            return "BudgetTrackApp()"

        self.root = root
        
        self.type_options = ["Income","Expense"]
        self.category_options = cat.BUDGET_CATEGORIES
        self.root.geometry("800x800")

        root.title("Budget Tracker")

        
        self.value_type = tk.StringVar(self.root)
        self.value_type.set("Choose an Expense Type")
        root.label_type = tk.OptionMenu(self.root,self.value_type, *self.type_options)
        root.label_type.grid(row=0, column=0)
        

        root.label_date = ttk.Label(self.root, text="Date (MM-DD-YY):")
        root.label_date.grid(row=1, column=0,pady=10)
        root.entry_date = ttk.Entry(self.root)
        root.entry_date.grid(row=1, column=1)

        root.label_desc = ttk.Label(self.root, text="Description:")
        root.label_desc.grid(row=2, column=0,pady=10)
        root.entry_desc = ttk.Entry(self.root)
        root.entry_desc.grid(row=2, column=1,pady=10)

        self.value_category = tk.StringVar(self.root)
        self.value_category.set("Choose a Category")
        root.label_category = tk.OptionMenu(self.root,self.value_category, *self.category_options)
        root.label_category.grid(row=3, column=0)

        root.label_amount = ttk.Label(self.root, text="Amount:")
        root.label_amount.grid(row=4, column=0, pady=10)
        root.entry_amount = ttk.Entry(self.root)
        root.entry_amount.grid(row=4, column=1, pady=10)

        root.submit_button = ttk.Button(self.root, text="Submit", command=self.submit)
        root.submit_button.grid(row=5, column=0,pady=10)

        root.view_button = ttk.Button(self.root, text="View Transactions",command=self.view_transactions)
        root.view_button.grid(row=6, column=0,pady=10)

        root.add_budget = ttk.Button(self.root, text="Add Budget",command=self.add_budget)
        root.add_budget.grid(row=7, column=0,pady=10)

        root.view_budget = ttk.Button(self.root, text="View Budget",command=self.check_budgets)
        root.view_budget.grid(row=8, column=0,pady=10)

    def run_app(self):
        self.root.mainloop()

    def submit(self):
        tran_type = self.root.label_type.cget("text")
        amount = self.root.entry_amount.get()
        date = self.root.entry_date.get()
        description = self.root.entry_desc.get()
        category = self.root.label_category.cget("text")

        
        try:
            transaction = tr.Transaction(tran_type,amount,date,category,description)
            add_row_to_csv("transactions.csv",[transaction.tran_type, transaction.amount, transaction.category, transaction.description, transaction.date])
            self.root.entry_amount.delete(0,tk.END)
            self.root.entry_date.delete(0,tk.END)
            self.root.entry_desc.delete(0,tk.END)
            self.value_type.set("Choose an Expense Type")
            self.value_category.set("Choose a Category")
            messagebox.showinfo("Success","Transaction added successfully")
            self.process_transaction_to_budget(transaction)
        except ValueError as e:
            messagebox.showerror("Error",e)

    def add_budget(self):
        BudgetWindow(self)


    def view_transactions(self):
        open_with_default_app("transactions.csv")

    def process_transaction_to_budget(self, transaction):
        with open('budgets.json', 'r') as file:
            data = json.load(file)  # Load list of budgets

        for budget in data:
            print(transaction.date.strftime("%B"))
            print(transaction.tran_type)
            
            if budget['month'] == transaction.date.strftime("%B"):
                category = transaction.category
                if category in budget['categories']:
                    if transaction.tran_type == "Expense":
                        budget['categories'][category] -= transaction.amount
                    else:
                        budget['categories'][category] += transaction.amount
                else:
                    budget['categories'][category] = transaction.amount  # Add new category if it doesn't exist

                # Write the updated data back to the file
                with open('budgets.json', 'w') as file:
                    json.dump(data, file, indent=4)
                return
            

    def check_budgets(self):
        with open('budgets.json', 'r') as file:
            data = json.load(file) 
        print("Checking budgets")
        for i,budget in enumerate(data):
            print(f"{i+1}. {budget}")


'''
Sub class of BudgetTrackApp that will handle the adding of budgets
'''
class BudgetWindow(tk.Toplevel):
    def __init__(self, budget_app):
        super().__init__(budget_app.root)
        self.budget_app = budget_app
        self.title("Add Budget")
        
        # Configure window
        self.geometry("800x800")
        self.category_entries = {}
        self.category_options = budget_app.category_options
        
        # Create and place widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Month entry
        self.label_month = ttk.Label(self, text="Month:")
        self.label_month.grid(row=0, column=0, pady=10, padx=5, sticky="w")
        self.entry_month = ttk.Entry(self)
        self.entry_month.grid(row=0, column=1, pady=10, padx=5, sticky="ew")
        
        # Create entries for each category
        for i, cat in enumerate(self.category_options):
            label = ttk.Label(self, text=cat)
            label.grid(row=i+1, column=0, pady=5, padx=5, sticky="w")
            
            entry = ttk.Entry(self)
            entry.grid(row=i+1, column=1, pady=5, padx=5, sticky="ew")
            self.category_entries[cat] = entry
            
        # Submit button
        self.submit_button = ttk.Button(
            self, 
            text="Submit", 
            command=self.submit_budget
        )
        self.submit_button.grid(
            row=len(self.category_options)+1, 
            column=0, 
            columnspan=2, 
            pady=20
        )
        
        # Configure grid columns
        self.grid_columnconfigure(1, weight=1)
        
    def submit_budget(self):
        month = self.entry_month.get()
        categories = {}
        
        # Collect all category values
        for cat, entry in self.category_entries.items():
            amount = entry.get()
            if amount:  # Only add if amount is provided
                categories[cat] = float(amount)
            else:
                categories[cat] = 0.0
                
        budget = bg.Budget(month, categories)
        budget_dict = budget.__dict__

        try:
            # Load existing data or create an empty list if the file doesn't exist or is empty
            try:
                with open('budgets.json', 'r') as file:
                    data = json.load(file)
                    if not isinstance(data, list):
                        data = [data]  # Convert to list if it’s a single budget dictionary
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            # Add the new budget to the list
            data.append(budget_dict)

            # Save the updated list back to the file
            with open('budgets.json', 'w') as file:
                json.dump(data, file, indent=4)

            messagebox.showinfo("Success", "Budget added successfully!")
            self.clear_entries()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def clear_entries(self):
        """Clear all entry fields"""
        self.entry_month.delete(0, tk.END)
        for entry in self.category_entries.values():
            entry.delete(0, tk.END)
