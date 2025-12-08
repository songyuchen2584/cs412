# File: mini_insta/urls.py
# Author: Song Yu Chen (songyu@bu.edu) 11/23/2025
# Description: URL page for the project app. 
from django.urls import path
from django.conf import settings
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # stores urls for different views

    # views without login requirement
    path('show_accounts', AccountListView.as_view(), name="show_accounts"),
    path('show_account/<int:pk>', AccountDetailView.as_view(), name="show_account"),
    ### account creation, login, logout
    path('create_account', CreateAccountView.as_view(), name='create_account'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name="logout"),
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name='logout_confirmation'),
    
]