# File: quotes/views.py
# Author: Song Yu Chen (songyu@bu.edu) 9/8/2025
# Description: Views page for the quotes app. 
import time
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
# Create your views here.

quotes =[
    # a list of quotes of Friedrich Nietzsche
    "To live is to suffer, to survive is to find some meaning in the suffering.",
    "Whoever fights monsters should see to it that in the process he does not become a monster. And if you gaze long enough into an abyss, the abyss will gaze back into you.",
    "He who has a why to live can bear almost any how.",
    "That which does not kill us makes us stronger.",
    "Without music, life would be a mistake.",
    "Hope in reality is the worst of all evils because it prolongs the torments of man.",
    "It is not a lack of love, but a lack of friendship that makes unhappy marriages.",
    ]

images=[
    # list of strings of links to images for Friedrich Nietzsche
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRa383UxltuzJtt2GAdqZTp71CnnsQ_invS-g&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTtmNhPjt4RxQErzNi2N3aO1VxILCs278P0A&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYYHCC8MEmvroG8mfi3Yp3N_-r9gC2qrm7yw&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9PKqslzJSVHqKZYmy20BO5DEDYxcYxz_-7Q&s",
    "data:image/jpeg;base64,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",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSviRZ9ZR2VsX7fAlMt-xGWDlLfKswiydqS8g&s",
    ]

def quote_page(request):
    "respond to the URL '', delegate work to a template."
    template_name = 'quotes/quote.html'
    # dict of content variables (key-value pairs)
    context = {
        "quote": random.choice(quotes),
        "picture": random.choice(images),
        "time": time.ctime,

    }
    return render(request, template_name, context)

def about_page(request):
    "respond to the URL 'about', delegate work to a template."
    
    template_name = 'quotes/about.html'
    # dict of content variables (key-value pairs)
    context = {
        "time": time.ctime(),

    }
    return render(request, template_name, context)

def show_all_page(request):
    "respond to the URL 'show_all', delegate work to a template."
    
    template_name = 'quotes/show_all.html'
    # dict of content variables (key-value pairs)
    context = {
        "time": time.ctime(),
        "quotes_nietzsche": quotes, 
        "images_nietzsche": images,

    }
    return render(request, template_name, context)
