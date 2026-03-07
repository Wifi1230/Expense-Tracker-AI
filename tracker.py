import csv
from collections import defaultdict
from datetime import datetime

class Expense:
    def __init__(self, item, price, category,date):
        self.item = item
        self.price = price
        self.category = category
        self.date=date

class BankAccount:
    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self._expenses= defaultdict(list)
        self.setup_csv()

    def setup_csv(self):
        try:
            with open(self.filename, 'x', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Item", "Price", "Category"])
        except FileExistsError:
            pass

    def add_expense (self,item,price,category):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_expense=Expense(item,price,category,date)
        self._expenses[category].append(new_expense)
        print(f"Added: {item} to {category}")

        with open(self.filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([date,item,price,category])
            
        print(f"\n[v] Saved to CSV: {item} (${price:.2f})")

    def __call__(self):
        print("\n--- EXPENSE REPORT ---")
        total = 0
        for category, list_of_expenses in self._expenses.items():
            for expense in list_of_expenses:
                print(f"[{expense.date}] [{category}] {expense.item}: ${expense.price:.2f}")
                total += expense.price
        print(f"----------------------\nTOTAL: ${total:.2f}")

def main():
    account = BankAccount()
    while True:
        print("\n1. Add item\n2. Show list\n3. Exit")
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
        elif choice=="3":
            print("Goodbye!")
            break
        else:
            print("Pick valid option (1-3)")
            continue
if __name__=="__main__":
    main()