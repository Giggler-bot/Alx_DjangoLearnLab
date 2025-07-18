from django.contrib import admin
from relationship_app.models import Book  # <- import from correct app

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'library')
    list_filter = ('library',)
    search_fields = ('title', 'author__name')
