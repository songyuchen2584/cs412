# File: mini_insta/views.py
# Author: Song Yu Chen (songyu@bu.edu) 9/23/2025
# Description: Views for the mini_insta app. 
import random
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.
class ProfileListView(ListView):
    ''' A view class to show all blog profiles'''
    
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''displays a single profile'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class RandomProfileDetailView(DetailView):
    '''displays a single random profile'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        ''' return one instance of the profile object at random'''

        all_profiles = Profile.objects.all()
        profile = random.choice(all_profiles)
        return profile




