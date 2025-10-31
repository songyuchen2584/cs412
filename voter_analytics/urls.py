# File: voter_analytics/urls.py
# Author: Song Yu Chen (songyu@bu.edu) 10/29/2025
# Description: URL page for the quotes app. 
from django.urls import path
from django.conf import settings
from .views import VoterListView, VoterDetailView, VoterGraphsView

urlpatterns = [
    # stores urls for different views,
    path(r'', VoterListView.as_view(), name="voters"),
    path(r'voters', VoterListView.as_view(), name="voters_list"),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
     path('graphs', VoterGraphsView.as_view(), name='graphs'),
]
