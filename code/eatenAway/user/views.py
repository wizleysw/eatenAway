from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .apis import APIAboutUser
from .tokens import Token


def RenderIntroPage(request):
    return render(request, 'intro.html', {})


def RenderMainPage(request):
    tk = Token(request.COOKIES.get('token'))
    tk_jwt_value = tk.decode_jwt()
    if tk_jwt_value is not None:
        username = tk_jwt_value['username']
        user_api = APIAboutUser(tk_jwt_value['username'])
        user_profile = user_api.get_user_profile()
        choice = user_api.get_user_preference()
        date_info, food_count = user_api.get_user_foodcount()
        return render(request, 'main.html',
                      {'username': username, 'foodcount': food_count, 'dateinfo': date_info,
                       'choice': choice, 'user_profile': user_profile})
    else:
        response = HttpResponseRedirect('/user/login')
        response.delete_cookie('token')
        return response


def RenderLoginPage(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        recaptcha = request.POST['g-recaptcha-response']

        user_api = APIAboutUser(username)
        token = user_api.get_user_token(password, recaptcha)

        if token is not None:
            response = HttpResponseRedirect('/user/main/')
            response.set_cookie('token', token)
            return response

        else:
            return render(request, 'login.html', {})

    else:
        tk = Token(request.COOKIES.get('token'))
        if tk.has_token():
            if tk.verify():
                response = HttpResponseRedirect('/user/main')
                return response
            response = HttpResponseRedirect('/user/login')
            response.delete_cookie('token')
            return response
        else:
            return render(request, 'login.html', {})


def RenderSignupPage(request):
    return render(request, 'signup.html', {})


def RenderEmailcheckPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        return render(request, 'waitemailcheck.html', {'username': username, 'email': email})
    else:
        return redirect('/user/signup/')
