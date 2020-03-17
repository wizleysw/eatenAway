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




