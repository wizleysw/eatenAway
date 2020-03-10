from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import requests


def checkTokenVerification(request):
    if (request.COOKIES.get('token')):
        url = "http://localhost:8000/api/token/verify/"
        r = requests.post(url, data={'token': request.COOKIES.get('token')})
        if (r.status_code == 400):
            return False
        if not r.json()['token']:
            return False
        else:
            return True
    return False


def introPage(request):
    return render(request, 'intro.html', {})


def mainPage(request):
    if (request.COOKIES.get('token')):
        if checkTokenVerification(request):
            return render(request, 'main.html', {})
        else:
            response = HttpResponseRedirect('/user/login')
            response.delete_cookie('token')
            return response
    else:
        return redirect('/user/intro/')


def login(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        recaptcha = request.POST['g-recaptcha-response']

        url = "http://localhost:8000/api/accounts/login/"
        r = requests.post(url, data={'username': username, 'password': password, 'g-recaptcha-response': recaptcha})

        if not r.json()['token']:
            return render(request, 'login.html', {})
        else:
            token = r.json()['token']
            response = HttpResponseRedirect('/user/main/')
            response.set_cookie('token', token)
            return response
    else:
        if(request.COOKIES.get('token')):
            if checkTokenVerification(request):
                response = HttpResponseRedirect('/user/main')
                return response
            else:
                response = HttpResponseRedirect('/user/login')
                response.delete_cookie('token')
                return response
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
