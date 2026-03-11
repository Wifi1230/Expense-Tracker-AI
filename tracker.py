import pandas as pd
import numpy as np
from datetime import datetime
import os

class BankAccount:
    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self.setup_csv()

    def setup_csv(self):
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=["Date", "Day", "Item", "Price", "Category"])
            df.to_csv(self.filename, index=False, encoding='utf-8')
    
    def load_data(self):
        try:
            df = pd.read_csv(self.filename)
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
            return df
        except Exception:
            return pd.DataFrame(columns=["Date", "Day", "Item", "Price", "Category"])

    def add_expense (self,item,price,category):
        date = datetime.now().strftime("%Y-%m-%d")
        day = datetime.now().strftime("%A")
        new_row = pd.DataFrame([[date, day, item, price, category]], columns=["Date", "Day", "Item", "Price", "Category"])
        new_row.to_csv(self.filename, mode='a', header=False, index=False, encoding='utf-8')
        print(f"\n[v] Added: {item} ({price:.2f} PLN)")

    def delete_expense(self):
        df = self.load_data()
        if df.empty:
            print("Nothing to delete.")
            return
        
        print("\n--- SELECT ITEM TO DELETE ---")
        print(df[["Date", "Item", "Price"]])

        try:
            choice = int(input("\nEnter Index number to delete (or -1 to cancel): "))
            if choice == -1: return
            
            df = df.drop(index=choice)
            df.to_csv(self.filename, index=False, encoding='utf-8')
            print(f"[v] Item deleted.")
            
        except (ValueError, KeyError):
            print("[!] Invalid index. Look at the numbers on the left.")

    def __call__(self):
        df = self.load_data()
        if df.empty:
            print("No expenses to show.")
            return
        
        print("\n--- EXPENSE REPORT ---")
        
        df['Date_dt'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date_dt').drop(columns=['Date_dt'])

        print("\n" + "="*70)
        print(f"{'DATE':<12} | {'ITEM':<20} | {'VALUE':>10} | {'CATEGORY'}")
        print("-" * 70)

        for _, row in df.iterrows():
            print(f"{row['Date']:<12} | {row['Item'][:20]:<20} | {row['Price']:>7.2f} PLN | {row['Category']}")
        
        total = df['Price'].sum()
        print("-" * 70)
        print(f"{'TOTAL:':<35} {total:>10.2f} PLN")

        if len(df) > 2:
            mean_val = np.mean(df['Price'])
            if df['Price'].max() > mean_val * 3:
                print("\n[!] INFO: AI ALERT: High-value transactions detected!")
        print("="*70)

def main():
    account = BankAccount()
    while True:
        print("\n1. Add item\n2. Show list\n3. Delete item\n4. Exit")
        choice = input("Choice: ")
        if choice=="1":
            while True:
                item = input("Item name: ").strip()
                price_raw = input("Price: ")
                category = input("Category: ").strip()
                try:
                    price = float(price_raw)
                    if not item or not category:
                        raise ValueError("Empty strings")
                    account.add_expense(item.capitalize(), float(price),category.capitalize())
                    break
                except ValueError:
                    print("\n[!] Error: Invalid price or empty fields. Try again.")
        elif choice=="2":
            account()
        elif choice == "3":
            account.delete_expense()
        elif choice=="4":
            print("Goodbye!")
            break
        else:
            print("Pick valid option (1-3)")
            continue
if __name__=="__main__":
    main()