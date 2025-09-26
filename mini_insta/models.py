# File: mini_insta/models.py
# Author: Song Yu Chen (songyu@bu.edu) 9/23/2025
# Description: Models for the mini_insta app. 
from datetime import timezone
from django.db import models

# Create your models here.
class Profile(models.Model):
    ''' Encapsulaes the data of a blog Article'''

    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(max_length=500, blank=True)
    join_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.display_name})"
    
    class Meta:
        ordering = ['-join_date']