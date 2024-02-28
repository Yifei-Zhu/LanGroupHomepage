
from django.urls import path

from .import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.submission_success, name='success_url'),

]
