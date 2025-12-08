# File: project/forms.py
# Author: Song Yu Chen (songyu@bu.edu) 11/30/2025
# Description: Froms page for the project app. 

from django import forms
from .models import Account

class CreateAccountForm(forms.ModelForm):
    ''' Form to handle account creation'''

    class Meta:
        ''' Associate form with the Account model from the database'''
        model = Account
        fields = ['username', 'biography', 'profile_picture'] 

class UpdateAccountForm(forms.ModelForm):
    '''Form to handle account updates'''
    
    class Meta:
        ''' Associate form with the Account model from the database'''
        
        model = Account
        fields = ['username', 'biography', 'profile_picture'] 