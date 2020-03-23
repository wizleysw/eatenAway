from django.shortcuts import render, redirect
import requests
from .models import Food
from eatenAway.settings import JWT_AUTH
import jwt, json
from user.views import checkTokenVerification

def menuDetail(request, foodname):
    if (request.COOKIES.get('token')):
        if checkTokenVerification(request):
            jwt_value = jwt.decode(request.COOKIES.get('token'), JWT_AUTH['JWT_SECRET_KEY'])
            url = "http://localhost:8000/api/food/user/"
            r = requests.post(url+jwt_value['username'], data={'foodname': foodname})
            try:
                chart = json.loads(r.json())
            except:
                chart = {'nope':1}

            url = "http://localhost:8000/api/food/"
            r = requests.get(url + foodname)
            if not r.status_code == 200:
                return redirect('/user/main/')
            menu = r.json()

            url = "http://localhost:8000/food/user/"
            return render(request, 'foodmenu.html', {'username':jwt_value['username'], 'menu': menu, 'chart': chart})

    else:
        return redirect('/user/intro/')


def addMenu(request):
    if(request.COOKIES.get('token')):
        if checkTokenVerification(request):
            return render(request, 'addmenu.html', {})
    else:
        return redirect('/user/intro')


def checkDateMenu(request):
    if(request.COOKIES.get('token')):
        if checkTokenVerification(request):
            jwt_value = jwt.decode(request.COOKIES.get('token'), JWT_AUTH['JWT_SECRET_KEY'])
            url = "http://localhost:8000/api/food/date/"
            r = requests.get(url + jwt_value['username'] + '/' + request.POST['date'])
            if not r.status_code == 200:
                dateres = {}
            else:
                dateres = r.json()

            return render(request, 'checkdatemenu.html', {'username':jwt_value['username'], 'date':request.POST['date'], 'Breakfast':dateres['B'], 'Lunch':dateres['L'], 'Dinner':dateres['D']})
    else:
        return redirect('/user/intro')


def updateDateMenu(request):
    if(request.COOKIES.get('token')):
        if checkTokenVerification(request):
            jwt_value = jwt.decode(request.COOKIES.get('token'), JWT_AUTH['JWT_SECRET_KEY'])
            url = "http://localhost:8000/api/food/date/"
            r = requests.post(url + jwt_value['username'], data=request.POST)
            if not r.status_code == 200:
                msg = '정보를 다시 확인해주세요.'

            else:
                msg = '요청이 정상적으로 반영되었습니다.'

            r = requests.get(url + jwt_value['username'] + '/' + request.POST['date'])
            if not r.status_code == 200:
                dateres = {}
            else:
                dateres = r.json()

            return render(request, 'updatedatemenu.html', {'msg':msg, 'date':request.POST['date'], 'Breakfast':dateres['B'], 'Lunch':dateres['L'], 'Dinner':dateres['D']})
