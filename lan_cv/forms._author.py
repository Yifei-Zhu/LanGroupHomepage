from django import forms
from .models import Author, Book, Paper


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'year', 'publisher',  'book_title', 'editor']

class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ['title', 'authors', 'year', 'journal_name', 'volume', 'page', 'url']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']