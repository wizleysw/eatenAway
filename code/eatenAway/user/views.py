from django.utils import timezone
import datetime
from .forms import AccountForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *


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
