from django.contrib import admin
from .models import  Book, Paper, Funding, Talk
from .forms import PaperForm, BookForm, FundingForm,TalkForm

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    form = PaperForm

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookForm

@admin.register(Funding)
class FundingAdmin(admin.ModelAdmin):
    form = FundingForm

@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    form = TalkForm
