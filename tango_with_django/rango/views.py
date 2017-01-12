from django.shortcuts import render
from rango.models import Category, Page


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    # Query the database for list of ALL categories currently stored.
    # Order the categories by number likes in descending order.
    # Retrieve the top only - or all if less than 5.
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'about_entries': {'title': 'About Rango', 'body': 'Rango is the cartoon person.'}}
    return render(request, 'rango/about.html', context=context_dict)
