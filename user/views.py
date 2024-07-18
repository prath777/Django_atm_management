from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome in to Prathmesh management system ")
# Create your views here.
