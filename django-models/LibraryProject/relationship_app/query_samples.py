from .models import Book, Author, Library, Librarian

# 1. List all books in a library
def list_books_in_library(library_id):
    return Book.objects.filter(library_id=library_id)

# 2. Query all books by a specific author
def books_by_author(author_id):
    return Book.objects.filter(author_id=author_id)

# 3. Retrieve the librarian for a library
def get_librarian_for_library(library_id):
    return Librarian.objects.get(library_id=library_id)
