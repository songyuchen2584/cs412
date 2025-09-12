# File: quotes/apps.py
# Author: Song Yu Chen (songyu@bu.edu) 9/8/2025
# Description: Apps page for the quotes app. 
from django.apps import AppConfig


class QuotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "quotes"
