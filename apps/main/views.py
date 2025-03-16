from django.shortcuts import render
from django.conf import settings
# from . import models


def media(request):
    return {'media':settings.MEDIA_URL}

def index(request):
    context = {

    }
    return render(request, 'main/index.html', context)


def contact(request):
    context = {

    }
    return render(request, 'main/contact.html', context)