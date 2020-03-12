from django.shortcuts import render, redirect
import requests
from .models import Food


def testPage(request, foodname):
    url = "http://localhost:8000/api/food/"
    r = requests.get(url+foodname)
    if not r.status_code == 200:
        return redirect('/user/intro/')
    menu = r.json()

    r = requests.post(url, data={'foodname': menu['menuname']})
    if r.status_code == 200:
        img = r.raw.read()
        print(len(img))

    return render(request, 'foodmenu.html', {'menu':menu})
