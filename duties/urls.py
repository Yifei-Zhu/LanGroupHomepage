from django.urls import path
from .views import show_groups

urlpatterns = [
    path('groups/', show_groups, name='show_groups'),
]
