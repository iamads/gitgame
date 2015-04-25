from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("This view if authenticated lists repo or provides login with github option")

def payload(request):
    return HttpResponse("This view receives the payload from github.")

def show(request):
    return HttpResponse("This view queries db of user payloads.")