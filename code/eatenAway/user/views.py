from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from itertools import chain

def index(request):
    return HttpResponse("HelloWorld from user!")

def getuser(request):
    account_info = Account.objects.order_by('account_no')
    user_info = User.objects.filter(id=account_info[0].user_info_id)
    return render(request, 'index.html',{'user_info' : account_info})