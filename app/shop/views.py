from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    text_var = 'hello this is index page'
    return HttpResponse(text_var)
