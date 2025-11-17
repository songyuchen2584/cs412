# File: dadjokes/models.py
# Author: Song Yu Chen (songyu@bu.edu) 11/11/2025
# Description: Models for the dadjokes app. 
from django.db import models
from django.urls import reverse

# Create your models here.
class Joke(models.Model):
    ''' Encapsulates data for the Jokes in the dadjokes app.'''

    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)


class Picture(models.Model):
    ''' Encapsulates data for the Pictures in the dadjokes app'''

    image_url = models.URLField(blank=True, max_length= 500)
    contributor = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)