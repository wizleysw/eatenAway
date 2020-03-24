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

            try:
                url = "http://localhost:8000/api/accounts/profile/"
                r = requests.get(url+jwt_value['username'])
                if r.status_code != 200:
                    user_profile = None
                else:
                    user_profile = json.loads(r.json())
            except:
                user_profile = None

            url = "http://localhost:8000/api/food/"
            r = requests.get(url + foodname)
            if not r.status_code == 200:
                return redirect('/user/main/')
            menu = r.json()

            url = "http://localhost:8000/food/user/"
            return render(request, 'foodmenu.html', {'username':jwt_value['username'], 'menu': menu, 'chart': chart, 'user_profile':user_profile})

    else:
        return redirect('/user/intro/')


def addMenu(request):
    if(request.COOKIES.get('token')):
        if checkTokenVerification(request):
            return render(request, 'addmenu.html', {})
    else:
        return redirect('/user/intro')


def checkDateMenu(request):
    if not request.POST:
        return redirect('/user/intro')

    if(request.COOKIES.get('token')):
        if checkTokenVerification(request):
            jwt_value = jwt.decode(request.COOKIES.get('token'), JWT_AUTH['JWT_SECRET_KEY'])
            url = "http://localhost:8000/api/food/date/"
            r = requests.get(url + jwt_value['username'] + '/' + request.POST['date'])
            dateres = r.json()
            return render(request, 'checkdatemenu.html', {'username':jwt_value['username'], 'date':request.POST['date'], 'Breakfast':dateres['B'], 'Lunch':dateres['L'], 'Dinner':dateres['D']})
    else:
        return redirect('/user/intro')


def updateDateMenu(request):
    if not request.POST:
        return redirect('/user/intro')

    if(request.COOKIES.get('token')):
        if checkTokenVerification(request):
            jwt_value = jwt.decode(request.COOKIES.get('token'), JWT_AUTH['JWT_SECRET_KEY'])
            url = "http://localhost:8000/api/food/date/"
            if request.POST['foodname'] == '삭제':
                r = requests.delete(url + jwt_value['username'] + '/' + request.POST['date'] + '/' + request.POST['mealkind'])
            else:
                r = requests.post(url + jwt_value['username'], data=request.POST)
            if r.status_code == 200 or r.status_code == 201:
                msg = '요청이 정상적으로 반영되었습니다.'
            else:
                msg = '정보를 다시 확인해주세요.'

            r = requests.get(url + jwt_value['username'] + '/' + request.POST['date'])
            dateres = r.json()
            if not r.status_code == 200:
                msg = '정보를 다시 확인해주세요.'

            return render(request, 'updatedatemenu.html', {'msg':msg, 'date':request.POST['date'], 'Breakfast':dateres['B'], 'Lunch':dateres['L'], 'Dinner':dateres['D']})
