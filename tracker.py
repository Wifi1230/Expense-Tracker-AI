from collections import defaultdict
class Expense:
    def __init__(self, item, price, category):
        self.item = item
        self.price = price
        self.category = category

class BankAccount:
    def __init__(self):
        self._expenses= defaultdict(list) 
    
    def add_expense (self,item,price,category):
        new_expense=Expense(item,price,category)
        self._expenses[category].append(new_expense)
        print(f"Added: {item} to {category}")

    def __call__(self):
        print("\n--- EXPENSE REPORT ---")
        total = 0
        for category, list_of_expenses in self._expenses.items():
            for expense in list_of_expenses:
                print(f"[{category}] {expense.item}: ${expense.price:.2f}")
                total += expense.price
        print(f"----------------------\nTOTAL: ${total:.2f}")

account = BankAccount()
account.add_expense("Pizza", 45, "Food")
account.add_expense("Bus Ticket", 5, "Transport")
account.add_expense("Burger", 25.5, "Food")
account()
