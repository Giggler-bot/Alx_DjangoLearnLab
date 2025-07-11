# delete.md

# Import the Book model
>>> from bookshelf.models import Book

# Retrieve and delete the book
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()

# Confirm the book is deleted
>>> Book.objects.all()
<QuerySet []>
