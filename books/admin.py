from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'author', 'cover_image', 'price', 'publish']
    list_display = ['id', 'title', 'author', 'publish']


admin.site.register(Book, BookAdmin)