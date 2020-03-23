from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from eatenAway.settings import JWT_AUTH
import requests, operator
import jwt, json


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
            jwt_value = jwt.decode(request.COOKIES.get('token'), JWT_AUTH['JWT_SECRET_KEY'])
            try:
                url = "http://localhost:8000/api/accounts/profile/"
                r = requests.get(url+jwt_value['username'])
                if r.status_code != 200:
                    user_profile = None
                else:
                    user_profile = json.loads(r.json())
            except:
                user_profile = None
            try:
                url = "http://localhost:8000/api/food/preference/"
                r = requests.get(url+jwt_value['username'])
                if r.status_code != 200:
                    choice = None
                else:
                    choice = r.json()
            except:
                choice = None
            url = "http://localhost:8000/api/food/user/"
            r = requests.get(url+jwt_value['username'])
            try:
                res = json.loads(r.json())
                food_count = sorted(res['foodcount'].items(), key=operator.itemgetter(1), reverse=True)
                return render(request, 'main.html', {'username':jwt_value['username'], 'foodcount':food_count, 'dateinfo':res['dateinfo'], 'choice':choice, 'user_profile':user_profile})
            except:
                return render(request, 'main.html', {'username':jwt_value['username'], 'choice':choice, 'user_profile':user_profile})
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
