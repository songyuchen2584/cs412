# File: mini_insta/serializers.py

from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    '''
    A serializer class for the the Post model.
    Specifies which fields are exposed in the API.
    '''

    class Meta:
        model = Post
        fields =['profile', 'caption']

    