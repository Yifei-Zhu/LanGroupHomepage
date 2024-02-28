from django.contrib import admin
from .models import Author, Book, Paper
from .forms import AuthorForm, PaperForm, BookForm

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'book_title', 'editor', 'display_authors')
    filter_horizontal = ('authors',)  # 这会为 'authors' 字段提供一个更易用的界面

    form = BookForm  # 这里应该是 BookForm
    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])
    display_authors.short_description = 'Authors'

class PaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'journal_name', 'volume', 'page', 'url', 'display_authors')
    filter_horizontal = ('authors',)  # 这会为 'authors' 字段提供一个更易用的界面

    form = PaperForm  # 这里应该是 PaperForm
    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])
    display_authors.short_description = 'Authors'

class AuthorAdmin(admin.ModelAdmin):
    form = AuthorForm

admin.site.register(Book, BookAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Author, AuthorAdmin)