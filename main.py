import sqlite3

# Create or connect to the database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID TEXT PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        ISBN TEXT,
        Status TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID TEXT PRIMARY KEY,
        Name TEXT,
        Email TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID TEXT PRIMARY KEY,
        BookID TEXT,
        UserID TEXT,
        ReservationDate DATE,
        FOREIGN KEY (BookID) REFERENCES Books (BookID),
        FOREIGN KEY (UserID) REFERENCES Users (UserID)
    )
''')

conn.commit()


def add_book():
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")

    cursor.execute("INSERT INTO Books VALUES (?, ?, ?, ?, ?)", (book_id, title, author, isbn, status))
    conn.commit()
    print("Book added successfully!")


def find_book_details():
    book_id = input("Enter BookID: ")
    cursor.execute('''
        SELECT Books.*, Users.Name, Reservations.ReservationDate
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
        WHERE Books.BookID = ?
    ''', (book_id,))

    book_details = cursor.fetchone()
    if book_details:
        print("Book Details:")
        print(f"BookID: {book_details[0]}")
        print(f"Title: {book_details[1]}")
        print(f"Author: {book_details[2]}")
        print(f"ISBN: {book_details[3]}")
        print(f"Status: {book_details[4]}")
        if book_details[5]:
            print(f"Reserved by: {book_details[5]}")
            print(f"Reservation Date: {book_details[6]}")
        else:
            print("Not reserved")
    else:
        print("Book not found")


def find_reservation_status():
    input_text = input("Enter BookID, Title, UserID, or ReservationID: ")

    if input_text.startswith("LB"):
        cursor.execute('''
            SELECT Books.BookID, Books.Status, Users.Name, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.BookID = ?
        ''', (input_text,))
    elif input_text.startswith("LU"):
        cursor.execute('''
            SELECT Books.BookID, Books.Status, Users.Name, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Users.UserID = ?
        ''', (input_text,))
    elif input_text.startswith("LR"):
        cursor.execute('''
            SELECT Books.BookID, Books.Status, Users.Name, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Reservations.ReservationID = ?
        ''', (input_text,))
    else:
        cursor.execute('''
            SELECT Books.BookID, Books.Status, Users.Name, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.Title = ?
        ''', (input_text,))

    results = cursor.fetchall()

    if results:
        for result in results:
            print(f"BookID: {result[0]}")
            print(f"Status: {result[1]}")
            print(f"Reserved by: {result[2]}")
            print(f"Reservation Date: {result[3]}")
    else:
        print("No matching records found")


def find_all_books():
    cursor.execute('''
        SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, Users.Name, Reservations.ReservationDate
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
    ''')

    books = cursor.fetchall()
    for book in books:
        print("BookID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])
        if book[5]:
            print("Reserved by:", book[5])
            print("Reservation Date:", book[6])
        else:
            print("Not reserved")
        print()


def update_book_details():
    book_id = input("Enter BookID to update: ")
    new_status = input("Enter new Status: ")

    cursor.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))
    cursor.execute("UPDATE Reservations SET ReservationDate = NULL WHERE BookID = ?", (book_id,))
    conn.commit()
    print("Book details updated successfully!")


def delete_book():
    book_id = input("Enter BookID to delete: ")

    cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
    cursor.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
    conn.commit()
    print("Book deleted successfully!")


while True:
    print("\nLibrary Management System Menu:")
    print("1. Add a new book")
    print("2. Find a book's detail")
    print("3. Find a book's reservation status")
    print("4. Find all books")
    print("5. Update book details")
    print("6. Delete a book")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        find_book_details()
    elif choice == "3":
        find_reservation_status()
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        update_book_details()
    elif choice == "6":
        delete_book()
    elif choice == "7":
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection
conn.close()
