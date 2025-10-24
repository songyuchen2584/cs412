# File: mini_insta/forms.py
# Author: Song Yu Chen (songyu@bu.edu) 9/30/2025
# Description: forms for the mini_insta app. 

from django import forms
from .models import Post, Profile
from django.forms.widgets import ClearableFileInput


class MultiFileInput(ClearableFileInput):
    allow_multiple_selected = True  # adds the 'multiple' attr

class MultiFileField(forms.FileField):
    def to_python(self, data):
        # data can be a list of uploaded files (for multiple=True)
        if not data:
            return []
        if isinstance(data, list):
            return data
        # Single file case
        return [data]

    def validate(self, data):
        # data is a list of files (possibly empty)
        if self.required and not data:
            raise forms.ValidationError(self.error_messages['required'], code='required')
        for file in data:
            super().validate(file)

class CreatePostForm(forms.ModelForm):
    ''' a form to add a create a new post to the database'''
    
    image_file = MultiFileField(
        widget=MultiFileInput(),
        label="Photos",
        required=True
    )
    class Meta:
        ''' associate this form with the post model from our database'''
        
        model = Post
        fields = ["caption", "image_file"]

class UpdateProfileForm(forms.ModelForm):
    '''A form to handle profile updates'''
    
    class Meta: 
        '''associate this form with the profile model from the database'''

        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']

class UpdatePostForm(forms.ModelForm):
    ''' A form to handle post updates'''
    
    class Meta:
        '''asscoiate this form with the post modile from the databse'''
        model = Post
        fields = ['caption'] 

class CreateProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image_url'] 
