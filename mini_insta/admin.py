# File: mini_insta/admin.py
# Author: Song Yu Chen (songyu@bu.edu) 9/23/2025
# Description: Admin for the mini_insta app. 
from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo, Follow, Comment, Like
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)