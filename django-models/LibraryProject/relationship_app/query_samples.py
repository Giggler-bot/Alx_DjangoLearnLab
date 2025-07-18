from relationship_app.models import Library, Author, Librarian, Book

# List all books in a specific library
def list_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.book_set.all()

# ✅ Updated: Query all books by a specific author
def list_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

# Retrieve the librarian for a specific library
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian
