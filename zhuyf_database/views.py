from django.shortcuts import render

# Create your views here.

def database_view(request):
    return render(request, 'zhuyf_database/database.html')