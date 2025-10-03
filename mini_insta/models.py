# File: mini_insta/models.py
# Author: Song Yu Chen (songyu@bu.edu) 9/23/2025
# Description: Models for the mini_insta app. 
from datetime import timezone
from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    ''' Encapsulates the data of a mini_insta Profile.'''

    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(max_length=500, blank=True)
    join_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.display_name})"
    
    def get_absolute_url(self):
        '''return a string representation of the url'''

        return reverse('article', kwargs={'pk':self.pk})
    
    def get_all_posts(self):
        '''Return the query-set of posts for this profile.'''

        posts = Post.objects.filter(profile = self)
        return posts
    
    class Meta:
        ordering = ['-join_date']

class Post(models.Model):
    ''' Encapsulates the data of a post.'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(max_length= 1000, blank=True)

    def __str__(self):
        ''' Return a string representation of this post'''
        return f"{self.caption}"
    
    def get_all_photos(self):
        '''Return the query-set of photos for this post.'''

        photos = Photo.objects.filter(post = self)
        return photos
    
    class Meta:
        ordering = ['-timestamp']


class Photo(models.Model):
    ''' Encapsulates the data of a photo for a post'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        ''' Return a string representation of the URL of the photo'''

        return f"{self.image_url}"        
    class Meta:
        ordering = ['-timestamp']
