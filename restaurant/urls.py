# File: restaurant/urls.py
# Author: Song Yu Chen (songyu@bu.edu) 9/16/2025
# Description: URL page for the restaurant app. 
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    # stores urls for different views,
    path(r'', views.main, name="main"),
    path(r'order', views.order, name="order"),
    path(r'confirmation', views.confirmation, name="confirmation"),
]
