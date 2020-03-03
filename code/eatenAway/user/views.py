from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from itertools import chain

def index(request):
    return HttpResponse("HelloWorld from user!")

def getuser(request):
    account_info = Account.objects.order_by('account_no')
    return render(request, 'index.html',{'user_info' : account_info})

def signup(request):
    return render(request, 'signup.html', {})