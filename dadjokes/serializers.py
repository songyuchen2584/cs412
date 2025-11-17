# File: dadjokes/serializers.py
# Author: Song Yu Chen (songyu@bu.edu) 11/11/2025
# Description: Serializers for the dadjokes app. 

from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    '''
    A serializer class for the the Joke model.
    Specifies which fields are exposed in the API.
    '''

    class Meta:
        model = Joke
        fields =['text', 'timestamp']

    def create(self, validated_data):
        '''handle object creattion'''

        print(f'JokeSerializer.create(), validated_data = {validated_data}.')

        # create an Object
        joke = Joke(**validated_data)

        # save to db 
        joke.save()

        return joke


class PictureSerializer(serializers.ModelSerializer):
    '''
    A serializer class for the the Picture model.
    Specifies which fields are exposed in the API.
    '''

    class Meta:
        model = Picture
        fields =['image_url', 'timestamp']
    
    def create(self, validated_data):
        '''handle object creation'''

        print(f'PictureSerializer.create(), validated_data = {validated_data}.')

        # create an Object
        picture = Picture(**validated_data)

        # save to db
        picture.save()

        return picture
