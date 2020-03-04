from django.utils import timezone
import datetime
from .forms import AccountForm
from django.http import HttpResponse, Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *


def signup(request):
    return render(request, 'signup.html', {})


def emailverify(request):
    dtime = datetime.datetime.now()

    if request.method == 'POST':
        form_data = AccountForm(request.POST)
        print(form_data)
        try:
            form_data.is_valid()
        except:
            pass


    return render(request, 'emailverify.html', {})