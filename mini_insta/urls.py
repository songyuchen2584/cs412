# File: mini_insta/urls.py
# Author: Song Yu Chen (songyu@bu.edu) 9/23/2025
# Description: URL page for the mini_insta app. 
from django.urls import path
from django.conf import settings
from . import views
from .views import ProfileListView, ProfileDetailView, RandomProfileDetailView, PostDetailView, CreatePostView

urlpatterns = [
    # stores urls for different views
    path('', RandomProfileDetailView.as_view(), name="random"),
    path('show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),
]
