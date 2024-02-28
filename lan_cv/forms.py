from django import forms
from .models import  Book, Paper, Funding, Talk


class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ['title', 'author', 'year', 'journal_name', 'volume', 'page', 'url', 'indexed']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'year', 'publisher',  'book_title', 'editor']

class FundingForm(forms.ModelForm):
    class Meta:
        model = Funding
        fields = ['title_in_Cn', 'source_in_En', 'source_in_Cn', 'category_in_En', 'category_in_Cn', 'start_year', 'start_month', 'end_year', 'end_month', 'total_funding','direct_funding']

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ['title', 'category_in_Cn', 'conference_in_CN', 'conference_in_EN', 'country_in_CN', 'city_in_CN', 'country_in_EN', 'city_in_EN', 'start_date',  'end_date']
