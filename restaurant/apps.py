# File: restaurant/apps.py
# Author: Song Yu Chen (songyu@bu.edu) 9/16/2025
# Description: Apps page for the restaurant app. 
from django.apps import AppConfig


class RestaurantConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "restaurant"
