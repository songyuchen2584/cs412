# File: mini_insta/urls.py
# Author: Song Yu Chen (songyu@bu.edu) 9/23/2025
# Description: URL page for the mini_insta app. 
from django.urls import path
from django.conf import settings
from . import views
from .views import ProfileListView, ProfileDetailView, RandomProfileDetailView, PostDetailView, CreatePostView, UpdateProfileView, DeletePostView , UpdatePostView, ShowFollowersDetailView, ShowFollowingDetailView, PostFeedListView

urlpatterns = [
    # stores urls for different views
    path('', RandomProfileDetailView.as_view(), name="random"),
    path('show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='update_post'),
    path('profile/<int:pk>/followers/', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following/', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/<int:pk>/feed', PostFeedListView.as_view(), name='show_feed'),
    path('profile/<int:pk>/search/', views.SearchView.as_view(), name='search'),
]
