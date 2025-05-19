books = []
def add_book(title, author, genre, isbn, status, read_status, progress, borrower=None, date=None):
    books.append({
        "title": title,
        "author": author,
        "genre": genre,
        "isbn": isbn,
        "status": status,
        "read_status": read_status,
        "progress": progress,
        "borrower": borrower,
        "date": date
    })
def update_progress(title, new_progress):
    for book in books:
        if book["title"].lower() == title.lower():
            book["progress"] = new_progress
            print("Updated ",title," progress to ",new_progress,"%")
            return
    print("Book not found!")

def search_by_genre(genre):
    print("Books in genre ",genre,":")
    for book in books:
        if book["genre"].lower() == genre.lower():
            print("-", book["title"], "by" ,book["author"], book["read_status"],":",book["progress"],"%")

def show_lent_books():
    print("Books currently lent out:")
    for book in books:
        if book["status"].lower() == "lent out":
            print("- ",book["title"],"to",book["borrower"],"since",book["date"])

def user_input():
    while True:
        print("\n Personal Library Management System\n 1) Add Book  2) Update Progress  3) Search by Genre  4) Show lent book 5) Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            title = input("Enter the title of book: ")
            author = input("Enter name of author: ")
            genre = input("Enter genre: ")
            isbn = input("Enter ISBN: ")
            status=input("Enter Status :")
            read_status=input("Enter read status: ")
            progress=input("Enter the progress:")
            if status.lower()=='lent out':
                borrower=input("Enter the name of borrower:")
                date=input("Enter date(YYYY-MM-DD):")
                add_book(title, author, genre, isbn, status, read_status, progress, borrower, date)
            else:
                add_book(title, author, genre, isbn, status, read_status, progress, borrower=None, date=None)
        elif choice == "2":
            title=input("Enter the title of book: ")
            progress=input("Enter the updated progress: ")
            update_progress(title, progress)
        elif choice == "3":
            genre=input("Enter the genre :")
            search_by_genre(genre)
        elif choice == "4":
            show_lent_books()
        elif choice =="5":
            break    
        else:
            print("Invalid choice! Please try again.")
user_input()