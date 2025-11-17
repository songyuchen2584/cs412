# File: mini_insta/urls.py
# Author: Song Yu Chen (songyu@bu.edu) 9/23/2025
# Description: URL page for the mini_insta app. 
from django.urls import path
from django.conf import settings
from . import views
from .views import CreateProfileView, MyProfileDetailView, PostListAPIView, ProfileListView, ProfileDetailView, RandomProfileDetailView, PostDetailView, CreatePostView, UpdateProfileView, DeletePostView , UpdatePostView, ShowFollowersDetailView, ShowFollowingDetailView, PostFeedListView, LogoutConfirmationView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # stores urls for different views
    path('', RandomProfileDetailView.as_view(), name="random"),
    path('show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('profile/create_post', CreatePostView.as_view(), name="create_post"),
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='update_post'),
    path('profile/<int:pk>/followers/', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following/', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/feed', PostFeedListView.as_view(), name='show_feed'),
    path('profile/search/', views.SearchView.as_view(), name='search'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name="logout"),
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name='logout_confirmation'),
    path('profile/', MyProfileDetailView.as_view(), name='my_profile'),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/follow', views.FollowProfileView.as_view(), name='follow_profile'),
    path('profile/<int:pk>/delete_follow', views.UnfollowProfileView.as_view(), name='unfollow_profile'),
    path('post/<int:pk>/like', views.LikePostView.as_view(), name='like_post'),
    path('post/<int:pk>/delete_like', views.UnlikePostView.as_view(), name='unlike_post'),

    ### API views:
    path ('api/posts/', PostListAPIView.as_view(), name='post_list_api'),
]
 



 