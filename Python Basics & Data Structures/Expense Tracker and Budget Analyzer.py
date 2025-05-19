expenses = []
budget_limits = {}  

def add_expense(date, amount, category, description, payment_method):
    expense = {
        "date": date,
        "amount": float(amount),
        "category": category.lower(),  
        "description": description,
        "payment_method": payment_method
    }
    expenses.append(expense)

def set_budget(category, limit):
    budget_limits[category.lower()] = float(limit)

def monthly_summary(category, year_month):
    category = category.lower()
    total_spent = 0
    transactions = 0

    for expense in expenses:
        if expense["category"] == category and expense["date"].startswith(year_month):
            total_spent += expense["amount"]
            transactions += 1

    if transactions == 0:
        print("No transactions found for "+ category +"in"+ year_month)
        return

    avg_transaction = total_spent / transactions
    total_expenses = sum(exp["amount"] for exp in expenses if exp["date"].startswith(year_month))
    percentage = (total_spent / total_expenses) * 100 if total_expenses > 0 else 0

    print("\nMonthly Summary for",category.capitalize(),year_month,":")
    print("- Total spent: $",total_spent)
    print("- Average per transaction: $",avg_transaction,":")
    print("- Number of transactions: ",transactions)
    print("- Percentage of monthly expenses: ",percentage,"%")

    if category in budget_limits and total_spent > budget_limits[category]:
        excess = total_spent - budget_limits[category]
        print("ALERT: You have exceeded your budget for",category,"by $",excess)

def user_input():

    while True:
        print("\nExpense Tracker and Budget Analyzer:\n 1) Add Expense  2) Set Budget  3) Monthly Summary  4) Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            amount = input("Enter amount: ")
            category = input("Enter category: ")
            description = input("Enter description: ")
            payment_method = input("Enter payment method: ")
            add_expense(date, amount, category, description, payment_method)

        elif choice == "2":
            category = input("Enter category to set budget for: ")
            limit = input("Enter budget limit: ")
            set_budget(category, limit)

        elif choice == "3":
            category = input("Enter category: ")
            year_month = input("Enter year and month (YYYY-MM): ")
            monthly_summary(category, year_month)

        elif choice == "4":
            break
        else:
            print("Invalid choice! Please try again.")

user_input()       