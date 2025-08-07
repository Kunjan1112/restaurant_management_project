from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.

def name(request):
    return HttpResponse("Hello My Name is Kunjan")

def index(request):
    return render(request,'home/home.html')

def login(request):
    return render(request,'home/login.html')

