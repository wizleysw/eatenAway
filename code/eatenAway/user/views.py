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
        # form_data = AccountForm(request.data)
        #
        # username = form_data.cleaned_data['username']
        # email = form_data.cleaned_data['email']
        username = 'abc'
        email = 'example@example.com'
        return render(request, 'waitemailcheck.html', {'username':username, 'email':email})
    except:
        pass
    # except:
    #     return redirect('/user/signup/')