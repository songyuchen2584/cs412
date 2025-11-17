# File: dadjokes/admin.py
# Author: Song Yu Chen (songyu@bu.edu) 11/11/2025
# Description: Admin for the dadjokes app. 
from .models import *
from django.contrib import admin

# Register your models here.
admin.site.register(Joke)
admin.site.register(Picture)