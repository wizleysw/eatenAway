from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from user.apis import APIAboutUser
from user.tokens import Token
from .apis import APIAboutFood


def RenderFoodPage(request, foodname):
    tk = Token(request.COOKIES.get('token'))
    tk_jwt_value = tk.decode_jwt()
    if tk_jwt_value is not None:
        username = tk_jwt_value['username']
        food_api = APIAboutFood(username, foodname)
        user_api = APIAboutUser(username)
        chart = food_api.get_user_food()
        user_profile = user_api.get_user_profile()
        menu = food_api.get_food_detail()
        return render(request, 'foodmenu.html',
                      {'username': username, 'menu': menu, 'chart': chart, 'user_profile': user_profile})
    else:
        response = HttpResponseRedirect('/user/login')
        response.delete_cookie('token')
        return response


def RenderAddMenuPage(request):
    tk = Token(request.COOKIES.get('token'))
    tk_jwt_value = tk.decode_jwt()
    if tk_jwt_value is not None:
        return render(request, 'addmenu.html', {})
    else:
        return redirect('/user/login')


def RenderCheckMenuByDatePage(request):
    if not request.POST:
        return redirect('/user/login')
    else:
        tk = Token(request.COOKIES.get('token'))
        tk_jwt_value = tk.decode_jwt()
        if tk_jwt_value is not None:
            username = tk_jwt_value['username']
            date = request.POST['date']
            food_api = APIAboutFood(username, None)
            dateres = food_api.get_user_food_by_date(date)
            return render(request, 'checkdatemenu.html',
                          {'username': username, 'date': date, 'Breakfast': dateres['B'],
                           'Lunch': dateres['L'], 'Dinner': dateres['D']})
        else:
            return redirect('/user/login')


def RenderUpdateMenuByDatePage(request):
    if not request.POST:
        return redirect('/user/intro')
    else:
        tk = Token(request.COOKIES.get('token'))
        tk_jwt_value = tk.decode_jwt()
        if tk_jwt_value is not None:
            username = tk_jwt_value['username']
            date = request.POST['date']
            mealkind = request.POST['mealkind']
            food_api = APIAboutFood(username, None)

            if request.POST['foodname'] == '삭제':
                msg = food_api.delete_user_food_by_date(date, mealkind)
            else:
                msg = food_api.update_user_food_by_date(request.POST)

            dateres = food_api.get_user_food_by_date(date)
            return render(request, 'updatedatemenu.html',
                          {'msg': msg, 'date': request.POST['date'], 'Breakfast': dateres['B'], 'Lunch': dateres['L'],
                           'Dinner': dateres['D']})

