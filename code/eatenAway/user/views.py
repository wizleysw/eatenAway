from django.utils import timezone
import datetime
from .forms import AccountForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
import requests

def mainPage(request):
    return render(request, 'index.html', {})


def login(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']
        recaptcha = request.POST['g-recaptcha-response']

        url = "http://localhost:8000/api/accounts/login/"
        r = requests.post(url, data={'username': username, 'password': password, 'csrfmiddlewaretoken': csrfmiddlewaretoken, 'g-recaptcha-response': recaptcha})
        print('LOGIN : ', r.status_code)
        print('LOGIN : ', r.text)

        return render(request, 'index.html', {})
    else:
        return render(request, 'login.html', {})

def signup(request):
    return render(request, 'signup.html', {})

def waitemailcheck(request):
    try:
        if(request.method == 'POST'):
            username = request.POST['username']
            email = request.POST['email']
            return render(request, 'waitemailcheck.html', {'username': username, 'email': email})
        else:
            return redirect('/user/signup/')
    except:
        return redirect('/user/signup/')
