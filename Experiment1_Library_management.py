class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_available = True

    def __str__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"{self.book_id}: {self.title} by {self.author} - {status}"


class Patron:
    def __init__(self, patron_id, name):
        self.patron_id = patron_id
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        self.borrowed_books.append(book)

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)


class Library:
    def __init__(self):
        self.books = {}
        self.patrons = {}

    def add_book(self, book):
        if book.book_id in self.books:
            print("A book with this ID already exists.")
            return

        self.books[book.book_id] = book
        print(f"Book '{book.title}' added successfully.")

    def register_patron(self, patron):
        if patron.patron_id in self.patrons:
            print("A patron with this ID already exists.")
            return

        self.patrons[patron.patron_id] = patron
        print(f"Patron '{patron.name}' registered successfully.")

    def borrow_book(self, book_id, patron_id):
        if book_id not in self.books:
            print("Book not found.")
            return

        if patron_id not in self.patrons:
            print("Patron not found.")
            return

        book = self.books[book_id]
        patron = self.patrons[patron_id]

        if not book.is_available:
            print(f"'{book.title}' is already borrowed.")
            return

        book.is_available = False
        patron.borrow_book(book)

        print(f"'{book.title}' borrowed by {patron.name}.")

    def return_book(self, book_id, patron_id):
        if book_id not in self.books:
            print("Book not found.")
            return

        if patron_id not in self.patrons:
            print("Patron not found.")
            return

        book = self.books[book_id]
        patron = self.patrons[patron_id]

        if book not in patron.borrowed_books:
            print(f"{patron.name} did not borrow '{book.title}'.")
            return

        book.is_available = True
        patron.return_book(book)

        print(f"'{book.title}' returned successfully.")

    def display_books(self):
        if not self.books:
            print("No books in the library.")
            return

        print("\n--- Library Books ---")
        for book in self.books.values():
            print(book)

    def display_patrons(self):
        if not self.patrons:
            print("No registered patrons.")
            return

        print("\n--- Registered Patrons ---")
        for patron in self.patrons.values():
            borrowed = [book.title for book in patron.borrowed_books]

            print(f"ID: {patron.patron_id}, Name: {patron.name}")
            print(f"Borrowed books: {borrowed if borrowed else 'None'}")


# -------------------------
# Example Usage
# -------------------------

library = Library()

# Add books
book1 = Book(1, "Python Programming", "John Smith")
book2 = Book(2, "Object-Oriented Programming", "Jane Doe")
book3 = Book(3, "Data Structures", "Robert Brown")

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)

# Register patrons
patron1 = Patron(101, "Alice")
patron2 = Patron(102, "Bob")

library.register_patron(patron1)
library.register_patron(patron2)

# Display books
library.display_books()

# Borrow books
library.borrow_book(1, 101)
library.borrow_book(2, 102)

# Try to borrow an unavailable book
library.borrow_book(1, 102)

# Display patron information
library.display_patrons()

# Return a book
library.return_book(1, 101)

# Display books again
library.display_books()
