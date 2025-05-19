tasks = []
priority_map = {"high": 1, "medium": 2, "low": 3}

def add_task(description, priority, due_date, status="Incomplete"):
    task = {"description": description, "priority": priority.lower(), "due_date": due_date, "status": status}
    tasks.append(task)

def mark_complete(description):
    for task in tasks:
        if task["description"].lower() == description.lower():
            task["status"] = "Complete"
            return
    print("Task not found!")

def search_tasks(keyword):
    return [task for task in tasks if keyword.lower() in task["description"].lower()]

def display_tasks():
    sorted_tasks = sorted(tasks, key=lambda x: (priority_map[x["priority"]], x["due_date"]))
    
    print("\nYour Tasks:")
    for task in sorted_tasks:
        print("-", task["description"], "| Priority:", task["priority"], "| Due:", task["due_date"], "| Status:", task["status"])

def user_input():
    while True:
        print("\nPersonal Task Manager:\n 1) Add Task  2) Mark Complete  3) Search  4) Display  5) Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            description = input("Enter task description: ")
            priority = input("Enter priority (High/Medium/Low): ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            add_task(description, priority, due_date)
        elif choice == "2":
            description = input("Enter task to mark as complete: ")
            mark_complete(description)
        elif choice == "3":
            keyword = input("Enter keyword to search: ")
            results = search_tasks(keyword)
            print("\nSearch Results:")
            for task in results:
                print("-", task["description"], "| Priority:", task["priority"], "| Due:", task["due_date"], "| Status:", task["status"])
        elif choice == "4":
            display_tasks()
        elif choice == "5":
            break
        else:
            print("Invalid choice! Please try again.")

user_input()
