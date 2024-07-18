from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("<center><h1>Welcome in to atm management system </h1></center>")
# Create your views here.
