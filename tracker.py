import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import IsolationForest
import os
MONITORED_CATEGORIES = {"food", "jedzenie",  "transport", "entertainment", "rozrywka"}

class BankAccount:
    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self.setup_csv()
        self.df = self.load_data()

    def setup_csv(self):
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=["Date", "Day", "Item", "Price", "Category"])
            df.to_csv(self.filename, index=False, encoding='utf-8')
    
    def load_data(self):
        try:
            return pd.read_csv(self.filename)
        except FileNotFoundError:
            return pd.DataFrame(columns=["Date", "Day", "Item", "Price", "Category"])
        
    def check_anomaly(self, price, category):
        df = self.df
        if df.empty:return

        if category not in MONITORED_CATEGORIES:return
        cat_df = df[df['Category'] == category]

        if len(cat_df) < 5: return
        
        prices = cat_df['Price'].values
        mean_val = np.mean(prices)
        std_val = np.std(prices,ddof=1)
        z_score = (price - mean_val) / std_val if std_val > 0 else 0
        if z_score > 2:
            print(f"\n[!] STATISTICAL ALERT: Z-Score is {z_score:.2f}")
            self.check_anomaly_ml(price, category)
        
    def check_anomaly_ml(self, price, category):
        if len(self.df) < 10: return

        df_ml = self.df.copy()
        df_ml['Day_num'] = pd.to_datetime(df_ml['Date']).dt.dayofweek
        X = df_ml[['Price', 'Day_num']]

        model = IsolationForest(contamination=0.1, random_state=42)
        model.fit(X)

        now_day_num = datetime.now().weekday()
        new_data = pd.DataFrame([[price, now_day_num]], columns=['Price', 'Day_num'])

        prediction = model.predict(new_data)
        decision_score = model.decision_function(new_data)

        print(f"\nML Analysis: Prediction={prediction[0]} | Anomaly Score={decision_score[0]:.4f}")
        
        if prediction[0] == -1:
            print(f"[!!!] ML ALERT: Isolation Forest confirmed this looks SUSPICIOUS! 🤖")
            print(f"This expense doesn't fit your usual patterns for this day of the week.")

    def add_expense (self,item,price,category):
        self.check_anomaly(price, category)
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        day = now.strftime("%A")
        new_row = pd.DataFrame([[date, day, item, price, category]], columns=["Date", "Day", "Item", "Price", "Category"])
        new_row.to_csv(self.filename, mode='a', header=False, index=False, encoding='utf-8')
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        print(f"\n[v] Added: {item} ({price:.2f} PLN)")

    def delete_expense(self):
        df = self.df
        if df.empty:
            print("Nothing to delete.")
            return
        
        df = df.reset_index(drop=True)
        print("\n--- SELECT ITEM TO DELETE ---")
        print(df[["Date", "Item", "Price"]])

        try:
            choice = int(input("\nEnter Index number to delete (or -1 to cancel): "))
            if choice == -1 or choice < 0 or choice >= len(df): return
            
            df = df.drop(index=choice)
            df.to_csv(self.filename, index=False, encoding='utf-8')
            self.df = df
            print(f"[v] Item deleted.")
            
        except (ValueError, KeyError):
            print("[!] Invalid index. Look at the numbers on the left.")

    def __call__(self):
        df = self.df.copy()
        if df.empty:
            print("No expenses to show.")
            return
        
        print("\n--- EXPENSE REPORT ---")
        
        df['Date_dt'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date_dt').drop(columns=['Date_dt'])

        print("\n" + "="*70)
        print(f"{'DATE':<12} | {'ITEM':<20} | {'VALUE':>10} | {'CATEGORY'}")
        print("-" * 70)

        for row in df.itertuples():
            print(f"{row.Date:<12} | {row.Item[:20]:<20} | {row.Price:>7.2f} PLN | {row.Category}")

        total = df['Price'].sum()
        total_typical = df[df['Category'].isin(MONITORED_CATEGORIES)]['Price'].sum()
        print("-" * 70)
        print(f"{'TOTAL EXPENSES:':<35} {total:>10.2f} PLN")
        print(f"{'  - TYPICAL (Lifestyle):':<35} {total_typical:>10.2f} PLN")
        print(f"{'  - OTHER (Fixed/Extra):':<35} {total - total_typical:>10.2f} PLN")

def main():
    account = BankAccount()
    while True:
        print("\n1. Add item\n2. Show list\n3. Delete item\n4. Exit")
        choice = input("Choice: ")
        if choice=="1":
            while True:
                item = input("Item name: ").strip()
                price_raw = input("Price: ")
                category = input("Category: ").strip().lower()
                try:
                    price = float(price_raw)
                    if price <= 0:
                        raise ValueError
                    if not item or not category:
                        raise ValueError("Empty strings")
                    account.add_expense(item, float(price),category)
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
            print("Pick valid option (1-4)")
            continue
if __name__=="__main__":
    main()