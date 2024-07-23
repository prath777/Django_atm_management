from django.shortcuts import render
from django.http import HttpResponse,JsonResponse 



















def home(request):
    return HttpResponse("<center><h1>Welcome in to atm management system </h1></center>")
# Create your views here.

def username(request):
    return HttpResponse("Enter your username")
def about(request):
    friends=[
        "amit","naman","ankit"
    ]
    return JsonResponse(friends,safe=False)


