from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book
from .models import Library
# Create your views here.

def list_all_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'