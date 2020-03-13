from django.shortcuts import render, redirect
import requests
from .models import Food


def testPage(request, foodname):
    url = "http://localhost:8000/api/food/"
    r = requests.get(url+foodname)
    if not r.status_code == 200:
        return redirect('/user/intro/')
    menu = r.json()

    return render(request, 'foodmenu.html', {'menu':menu})
