# advanced_features_and_security/bookshelf/forms.py

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date'] # Exclude added_by as it's set in view