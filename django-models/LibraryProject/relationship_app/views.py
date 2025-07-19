from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book
# Create your views here.

def list_all_books(request):
    books = Book.object.all()
    return render(request, 'list_book.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'