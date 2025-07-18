from relationship_app.models import Library, Author, Librarian

# List all books in a specific library
def list_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.book_set.all()  # OR library.books.all() if related_name="books" is set in Book model

# Query all books by a specific author
def list_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return author.book_set.all()

# Retrieve the librarian for a specific library
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian

    return Book.objects.filter(author=author)