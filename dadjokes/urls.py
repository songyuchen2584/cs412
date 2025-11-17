# File: dadjokes/urls.py
# Author: Song Yu Chen (songyu@bu.edu) 11/11/2025
# Description: URL page for the dadjokes app. 
from django.urls import path
from django.conf import settings
from .views import JokeDetailAPIView, JokeDetailView, JokeListAPIView, JokeListView, PictureDetailAPIView, PictureDetailView, PictureListAPIView, PictureListView, RandomJokeAPIView, RandomJokePictureView, RandomPictureAPIView

urlpatterns = [
    # stores urls for different views,
    path('api/jokes', JokeListAPIView.as_view(), name="joke_list_api"),
    path("api/",RandomJokeAPIView.as_view(), name="api_random_joke"),
    path("api/random", RandomJokeAPIView.as_view(), name="api_random_joke_alias"),
    path("api/joke/<int:pk>", JokeDetailAPIView.as_view(), name="api_joke_detail"),
    path("api/pictures/", PictureListAPIView.as_view(), name="api_pictures"),
    path("api/picture/<int:pk>", PictureDetailAPIView.as_view(), name="api_picture_detail"),
    path("api/random_picture", RandomPictureAPIView.as_view(), name="api_random_picture"),
    
    path('', RandomJokePictureView.as_view(), name ="home"),
    path('random', RandomJokePictureView.as_view(), name="random"),
    path("jokes/", JokeListView.as_view(), name="jokes"),
    path("joke/<int:pk>/", JokeDetailView.as_view(), name="joke_detail"),
    path("pictures/", PictureListView.as_view(), name="pictures"),
    path("picture/<int:pk>/", PictureDetailView.as_view(), name="picture_detail"),
    
]
