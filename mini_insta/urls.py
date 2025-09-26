# File: mini_insta/urls.py
# Author: Song Yu Chen (songyu@bu.edu) 9/23/2025
# Description: URL page for the mini_insta app. 
from django.urls import path
from django.conf import settings
from . import views
from .views import ProfileListView, ProfileDetailView, RandomProfileDetailView

urlpatterns = [
    # stores urls for different views
    path('', RandomProfileDetailView.as_view(), name="random"),
    path('show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
]
