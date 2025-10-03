# File: mini_insta/forms.py
# Author: Song Yu Chen (songyu@bu.edu) 9/30/2025
# Description: forms for the mini_insta app. 

from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    ''' a form to add a create a new post to the database'''
    image_url = forms.URLField(label="Photo URL", required=True)

    class Meta:
        ''' associate this form with the post model from our database'''
        model = Post
        fields = ["caption"]