# File: restaurant/views.py
# Author: Song Yu Chen (songyu@bu.edu) 9/16/2025
# Description: Views page for the restaurant app. 
import random
from django.shortcuts import render
from django.http import HttpResponse
import time

# Create your views here.
def main(request):
    '''Respond to the URL '', goes to the main page of the restaurant app.'''
    
    template_name = "restaurant/main.html"

    context = {
        # dictionary of context variables
        "time": time.ctime,
    }
    return render(request, template_name, context)

def order(request):
    ''' Responds to the URL 'order', goes to the order page of the restaurant app.'''
    
    template_name = "restaurant/order.html"

    daily_specials = [
        # list of lists to share daily specials and their price
        ["Pie Poppers", "6"],
        ["Chicken Fill Up", "10"],
        ["Double Mash Meal", "12"],
        ["Fan Favorites Box", "20"],
        ["Taste of KFC 6 pc.", "15"],
    ]

    # choose daily special
    daily_special = random.choice(daily_specials)

    context = {
        # dictionary of context variables
        "time": time.ctime,
        "special_item": daily_special[0],
        "special_price": daily_special[1],
    }
    return render(request, template_name, context)


def confirmation(request):
    ''' 
    Respond to the URL 'confirmation' goes to the confirmation page of the 
    restaurant app after havin received an order
    '''

    template_name = "restaurant/confirmation.html"
    print(request)

    # check to see if a POST request was sent with POST message
    if request.POST:
        # extract from fields of form into variables

        # contact info
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        # checkboxes
        wings_and_wedges = request.POST.get('wings_and_wedges')
        famous_bowl = request.POST.get('famous_bowl')
        hot_wings = request.POST.get('hot_wings')
        wedges = request.POST.get('wedges')
        # option for spiciness of wings
        spiciness = request.POST.get('spiciness')
        # special instructions
        instructions = request.POST['instructions']
        # daily special passed through hidden field
        special_item = request.POST.get("special_item")
        special_price = request.POST.get("special_price")
        # check if daily special was picked
        special = request.POST.get("special")


    # calculate cost of items
    cost = 0
    if wings_and_wedges:
        cost +=6
    if famous_bowl:
        cost+=5
    if hot_wings:
        cost+=4
    if wedges:
        cost+=2
    if special:
        cost+= float(special_price)
    # calculate the tax
    tax = round(cost * .07, 2)
    total = tax + cost

    # create random ready time
    minutes_to_add = random.randint(30, 60)
    wait_seconds = minutes_to_add * 60

    # current time in seconds
    now_seconds = time.time()

    # add wait time
    ready_time_seconds = now_seconds + wait_seconds

    # format nicely with ctime
    ready_time = time.ctime(ready_time_seconds)

    context = {
        # dictionary of context variables for the confiration page
        "cost": cost,
        "wings_and_wedges": wings_and_wedges,
        "famous_bowl": famous_bowl,
        "hot_wings": hot_wings,
        "wedges": wedges,
        "cost": cost,
        "name": name,
        "phone": phone,
        "email": email,
        "spiciness": spiciness,
        "instructions": instructions,
        "tax": tax,
        "total": total,
        "ready_time": ready_time,
        "special_item": special_item,
        "special_price": special_price,
        "special": special,
    }


    return render(request, template_name, context)