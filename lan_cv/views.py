from django.shortcuts import render,  redirect
from .models import Talk, Funding


def lan_view(request):
    print("This line should print to the console.")
    talks = Talk.objects.all().order_by('-start_date')
    fundings = Funding.objects.all().order_by('-start_year', '-start_month')
    for funding in fundings:
        funding.total_funding *= 10000
        funding.total_funding = "{:,}".format(funding.total_funding)
    return render(request, 'lan_cv/lan_cv.html', {'talks': talks,'fundings': fundings})

def publication_view(request):
    return render(request, 'lan_cv/publication.html')


from itertools import groupby

from .models import Paper, Book

def publication(request):
    papers = Paper.objects.all().order_by('-year')
    books = Book.objects.all().order_by('-year')

    grouped_papers = {year: list(group) for year, group in groupby(papers, key=lambda x: x.year)}
    grouped_books = {year: list(group) for year, group in groupby(books, key=lambda x: x.year)}

    return render(request, 'lan_cv/publication.html', {'grouped_papers': grouped_papers, 'grouped_books': grouped_books})
