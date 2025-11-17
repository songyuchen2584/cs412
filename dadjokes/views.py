import random
from urllib import response
from django.shortcuts import render

# Create your views here.

###---------------API-----------------###
from rest_framework import generics
from .serializers import *
from django.views.generic import DetailView, TemplateView, ListView

class JokeListAPIView(generics.ListCreateAPIView):
    '''
    This view will expose the API for Jokes with List and Create
    '''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListCreateAPIView):
    '''
    This view will expose the API for Pictures with List and Create
    '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class JokeDetailAPIView(generics.RetrieveAPIView):
    """
    'api/joke/<int:pk>' – GET a single Joke by pk.
    """
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureDetailAPIView(generics.RetrieveAPIView):
    """
    'api/picture/<int:pk>' – GET a single Picture by pk.
    """
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class RandomJokeAPIView(generics.ListAPIView):
    """
    'api/' and 'api/random' – GET one random Joke as JSON.
    """

    def get(self, request, *args, **kwargs):
        jokes = list(Joke.objects.all())
        if not jokes:
            return response({"detail": "No jokes available"}, status=404)

        joke = random.choice(jokes)
        serializer = JokeSerializer(joke)
        return response(serializer.data)


class RandomPictureAPIView(generics.ListAPIView):
    """
    'api/random_picture' – GET one random Picture as JSON.
    """

    def get(self, request, *args, **kwargs):
        pictures = list(Picture.objects.all())
        if not pictures:
            return response({"detail": "No pictures available"}, status=404)

        picture = random.choice(pictures)
        serializer = PictureSerializer(picture)
        return response(serializer.data)



###--------------HTML-------------###

class RandomJokePictureView(TemplateView):
    '''
    View for displaying a random Joke and Picture
    '''

    model = Joke
    template_name="dadjokes/home.html"
    context_object_name='joke'

    def get_context_data(self, **kwargs):
        '''
        Get a random joke and picture
        '''
        objects ={}
        
        all_jokes = Joke.objects.all()
        objects['joke'] = random.choice(all_jokes)
        
        all_pictures = Picture.objects.all()
        objects['picture'] = random.choice(all_pictures)

        return objects

class JokeListView(ListView):
    """
    'jokes' – show a page with all Jokes (HTML, no images).
    """
    model = Joke
    template_name = "dadjokes/joke_list.html"
    context_object_name = "jokes"
    ordering = ['-created_at']


class JokeDetailView(DetailView):
    """
    'joke/<int:pk>' – show one Joke by its primary key (HTML).
    """
    model = Joke
    template_name = "dadjokes/joke_detail.html"
    context_object_name = "joke"

class PictureListView(ListView):
    """
    'pictures' – show a page with all Pictures (HTML).
    """
    model = Picture
    template_name = "dadjokes/picture_list.html"
    context_object_name = "pictures"
    ordering = ['-created_at']


class PictureDetailView(DetailView):
    """
    'picture/<int:pk>' – show one Picture by its primary key (HTML).
    """
    model = Picture
    template_name = "dadjokes/picture_detail.html"
    context_object_name = "picture"
