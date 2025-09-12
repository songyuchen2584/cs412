# File: quotes/urls.py
# Author: Song Yu Chen (songyu@bu.edu) 9/8/2025
# Description: URL page for the quotes app. 
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    # stores urls for different views,
    path(r'', views.quote_page, name="quote"),
    path(r'quote', views.quote_page, name="quote"),
    path(r'about', views.about_page, name="about"),
    path(r'show_all', views.show_all_page, name="show_all"),
]
