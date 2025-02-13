import tkinter as tk
import budget_tracker_app as bt 
import pandas as pd

def main():
    try:
        df = pd.read_csv("transactions.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["TranType","Amount", "Category", "Description" , "Date"])
        df.to_csv("transactions.csv", index=False)

    root = tk.Tk()
    app = bt.BudgetTrackApp(root)
    app.run_app()



if __name__ == "__main__":
    main()