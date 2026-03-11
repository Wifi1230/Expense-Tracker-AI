import csv
from collections import defaultdict
from datetime import datetime

class Expense:
    def __init__(self, item, price, category,date,day):
        self.item = item
        self.price = price
        self.category = category
        self.date=date
        self.day=day

class BankAccount:
    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self._expenses= defaultdict(list)
        self.setup_csv()
        self.load_data()

    def setup_csv(self):
        try:
            with open(self.filename, 'x', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Day", "Item", "Price", "Category"])
        except FileExistsError:
            pass
    
    def load_data(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    new_exp = Expense(
                        item=row['Item'],
                        price=float(row['Price']),
                        category=row['Category'],
                        date=row['Date'],
                        day=row['Day']
                    )
                    self._expenses[row['Category']].append(new_exp)
        except (FileNotFoundError, StopIteration):
            pass

    def add_expense (self,item,price,category):
        date = datetime.now().strftime("%Y-%m-%d")
        day = datetime.now().strftime("%A")
        new_expense=Expense(item,price,category,date,day)
        self._expenses[category].append(new_expense)
        print(f"Added: {item} to {category}")

        with open(self.filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([date,day,item,price,category])
            
        print(f"\n[v] Saved to CSV: {item} ({price:.2f})PLN")

    def delete_expense(self):
        all_exps = []
        for cat in self._expenses:
            for e in self._expenses[cat]:
                all_exps.append(e)
        
        if not all_exps:
            print("Nothing to delete.")
            return

        print("\n--- SELECT ITEM TO DELETE ---")
        for i, e in enumerate(all_exps):
            print(f"{i+1}. {e.date} | {e.item} - {e.price} PLN")
        
        try:
            choice = int(input("\nEnter number to delete (or -1 to cancel): "))
            if choice == -1: return
            
            to_remove = all_exps[choice-1]
            
            self._expenses[to_remove.category].remove(to_remove)
            
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Day", "Item", "Price", "Category"])
                for cat in self._expenses:
                    for e in self._expenses[cat]:
                        writer.writerow([e.date, e.day, e.item, e.price, e.category])
            
            print(f"[v] Deleted: {to_remove.item}")
            
        except (ValueError, IndexError):
            print("[!] Invalid selection.")

    def __call__(self):
        print("\n--- EXPENSE REPORT ---")

        all_expenses = []
        for list_of_expenses in self._expenses.values():
            all_expenses.extend(list_of_expenses)
        
        if not all_expenses:
            print("No expenses to show.")
            return
        
        all_expenses.sort(key=lambda x: datetime.strptime(x.date, "%Y-%m-%d"))

        total = 0
        for expense in all_expenses:
            print(f"{expense.date} ({expense.day[:3]}) | {expense.item[:20]:<20}|{expense.price:>8.2f} PLN")
            total += expense.price
        print(f"----------------------\nTOTAL: {total:.2f}PLN")

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