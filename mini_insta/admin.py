# File: mini_insta/admin.py
# Author: Song Yu Chen (songyu@bu.edu) 9/23/2025
# Description: Admin for the mini_insta app. 
from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile)