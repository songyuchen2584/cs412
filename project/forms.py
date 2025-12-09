# File: project/forms.py
# Author: Song Yu Chen (songyu@bu.edu) 11/30/2025
# Description: Froms page for the project app. 

from django import forms
from .models import Account, Bid, Product
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

class CreateProductForm(forms.ModelForm):
    ''' Form to handle product listing'''

    image_file = MultiFileField(
        widget=MultiFileInput(),
        label="Photos",
        required=False
    )

    class Meta:
        ''' Associate form with the Product model from the database'''
        
        model = Product
        fields = ['name', 'description', 'category', 'expected_price']

class UpdateProductForm(forms.ModelForm):
    '''Form to handle the update of product information'''

    class Meta:
        ''' Associate form with the Product model from the database'''
        
        model = Product
        fields = ['name', 'description', 'image', 'category', 'expected_price', 'status']

class CreateBidForm(forms.ModelForm):
    '''Form to handle bid creation'''

    class Meta:
        ''' Associate form with the Bid model from the database'''
        model = Bid
        fields = ['message', 'bid_price']

class RateProductForm(forms.Form):
    '''From to handle rating purchased products, from 1-5'''
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        label="Rating (1–5 Stars)"
    )
