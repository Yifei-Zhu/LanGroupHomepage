from django.urls import path

from . import views

urlpatterns = [
    path('lan/', views.lan_view, name='lan_view'),
    path('publication/', views.publication, name='publication'),

]

