from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
author = Author.objects.get(name='John Doe')
books_by_author = Book.objects.filter(author=author)
print("Books by John Doe:")
for book in books_by_author:
    print(book.title)

# List all books in a library
library = Library.objects.get(name='City Library')
books_in_library = library.books.all()
print("Books in City Library:")
for book in books_in_library:
    print(book.title)

# Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)
print(f"Librarian of {library.name}: {librarian.name}")
