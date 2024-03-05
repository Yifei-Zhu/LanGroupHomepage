"""
URL configuration for myresearchgroup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/custom_login.html'), name='login'),

    path('user_panel/', views.user_panel_view, name='user_panel'),
    
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # # path('login/', LoginView.as_view(next_page='/'), name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),


    path('add_event/', views.add_event, name='add_event'),
    path('events/', views.events, name='events'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),

    path('calendar/', auth_views.LoginView.as_view(template_name='registration/user_panel.html'), name='calendar'),

    path('todolist/', auth_views.LoginView.as_view(template_name='registration/todo_list.html'), name='todolist'),

    path('event/<int:event_id>/status/', views.update_event_status, name='update_event_status'),
    
    path('todos/', views.load_todos, name='load_todos'),
    path('todo/', views.add_todo, name='add_todo'),
    path('todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('update_todo_order/', views.update_todo_order, name='update_todo_order'),
    path('toggle-todo-completed/<int:todo_id>/', views.toggle_todo_completed, name='toggle_todo_completed'),

]


