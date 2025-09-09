import time
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.


def home_page(request):
    "respond to the URL '', delegate work to a template."
    template_name = 'quotes/quote.html'
    # dict of content variables (key-value pairs)
    context = {
        "time": time.ctime(),

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
