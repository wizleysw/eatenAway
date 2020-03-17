from rest_framework.authentication import BasicAuthentication
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.forms import AccountForm
from django.http import Http404, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccountSerializer
from user.models import Account
from food.models import Food, DailyUserFood
from eatenAway.settings import GOOGLE_RECAPTCHA_SECRET_KEY
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.core import serializers
import requests
import urllib
import json
import datetime


def checkRecaptcha(recaptcha_response):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())

    if not result['success']:
        return False

    return True


"""
회원가입 폼 검증 및 등록:
POST /api/accounts/
"""
class AccountList(APIView):
    def get(self, request):
        return Response('HelloWorld')

    def post(self, request):
        form_data = AccountForm(request.data)

        if not checkRecaptcha(request.data['g-recaptcha-response']):
            return Response("fail.", status=HTTP_400_BAD_REQUEST)

        if form_data.is_valid():
            cl = VerifyExistence()
            ac = VerifyExistence.getObject_with_username(cl, form_data.cleaned_data['username'])
            if not AccountSerializer(ac).validate_username(form_data.cleaned_data['username']):
                return Response('fail.', status=HTTP_400_BAD_REQUEST)

            ac = VerifyExistence.getObject_with_email(cl, form_data.cleaned_data['email'])
            if not AccountSerializer(ac).validate_email(form_data.cleaned_data['email']):
                return Response('fail.', status=HTTP_400_BAD_REQUEST)

            new_account = form_data.save(commit=False)
            new_account.set_password(form_data.cleaned_data['password'])
            new_account.save()

            user = Account.objects.get(username=form_data.cleaned_data['username'])
            message = render_to_string('activate.html', {
                'domain': 'localhost:8000',
                'username': form_data.cleaned_data['username'],
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })

            mail_subject = 'eaten-Away 이메일 인증'
            to_email = form_data.cleaned_data['email']
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return Response('success.', status=HTTP_201_CREATED)

        else:
            return Response('fail.', status=HTTP_400_BAD_REQUEST)


"""
id 중복 검사 : 
GET /api/accounts/verify/<str:id>/

email 중복 검사 : 
POST /api/accounts/verify/
"""
class VerifyExistence(APIView):
    def getObject_with_username(self, username):
        try:
            return Account.objects.get(username=username)
        except Account.DoesNotExist:
            return "OK"

    def getObject_with_email(self, email):
        try:
            return Account.objects.get(email=email)
        except Account.DoesNotExist:
            return "OK"

    def get(self, request, username):
        ac = self.getObject_with_username(username)
        if ac == "OK":
            return Response("사용가능한 아이디입니다.")
        else:
            if AccountSerializer(ac).validate_username(username):
                return Response("사용가능한 아이디입니다.")
            else:
                return Http404

    def post(self, request):
        email = request.data['email']
        ac = self.getObject_with_email(email)
        if ac == "OK":
            return Response("사용가능한 이메일입니다.")
        if AccountSerializer(ac).validate_email(email):
            return Response("사용가능한 이메입니다.")
        else:
            return Http404


class EmailActivate(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except:
            user = None
        try:
            if user is not None and account_activation_token.check_token(user, token):
                user.status = 'O'
                user.active = True
                user.save()
                return render(request, 'emailverifysuccess.html', {'result': True})
            else:
                return render(request, 'emailverifysuccess.html', {'result': False})
        except:
            return render(request, 'emailverifysuccess.html', {'result': False})


"""
post : login
delete : logout
"""
class AccountAuthentication(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def authenticateAccount(self, username, password):
        try:
            AccountInfo = Account.objects.get(username=username)

            if check_password(password, AccountInfo.password):
                if AccountInfo.status == 'O':
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def post(self, request):
        if not checkRecaptcha(request.data['g-recaptcha-response']):
            return Response("fail.", status=HTTP_400_BAD_REQUEST)

        username = request.data['username']
        password = request.data['password']

        if self.authenticateAccount(username=username, password=password):
            url = "http://localhost:8000/api/token/"
            r = requests.post(url, data={'username': username, 'password': password})
            if not r.json()['token']:
                return Response('fail', status=HTTP_400_BAD_REQUEST)
            else:
                token = r.json()['token']
                return Response({'token': token}, status=HTTP_200_OK)
        else:
            return Response('fail.', status=HTTP_400_BAD_REQUEST)

        return Response('failed', status=HTTP_400_BAD_REQUEST)


'''
get : 음식 정보
post : 음식 사진 정보
'''
class FoodList(APIView):
    # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, foodname):
        if not foodname:
            return Response(status=HTTP_400_BAD_REQUEST)
        try:
            menu = Food.objects.get(menuname=foodname)
            data = {
                'menuname': menu.menuname,
                'category': menu.category,
                'country': menu.country,
                'taste': menu.taste,
                'stock': menu.stock,
                'description': menu.description
                # 'profile': menu.profile
            }
            return Response(data, status=HTTP_200_OK)

        except:
            return Response('fail', status=HTTP_400_BAD_REQUEST)

    def post(self, request):
        if not request.data['foodname']:
            return Response(status=HTTP_400_BAD_REQUEST)
        try:
            img = Food.objects.get(menuname=request.data['foodname']).profile
            return HttpResponse(img, content_type='*/*', status=HTTP_200_OK)
        except:
            return Response('fail', status=HTTP_400_BAD_REQUEST)

"""
get : 이 주간 먹은 메뉴 개수 리턴
"""

class UserDailyFoodList(APIView):
    # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, username):
        if not username:
            return Response(HTTP_400_BAD_REQUEST)
        try:
            data = DailyUserFood.objects.filter(username=username, date__range=[datetime.date.today() - datetime.timedelta(days=9), datetime.date.today()])
            if not data.exists():
                return Response('no info', HTTP_400_BAD_REQUEST)
            else:
                res = dict()
                foodcount = dict()
                dateinfo = dict()
                for row in data:

                    if not row.food in foodcount:
                        foodcount[row.food] = 1
                    else:
                        foodcount[row.food] +=1

                    if not str(row.date) in dateinfo:
                        dateinfo[str(row.date)] = dict()
                        dateinfo[str(row.date)][row.mealkind] = row.food

                    else:
                        dateinfo[str(row.date)][row.mealkind] = row.food

                res['foodcount'] = foodcount
                res['dateinfo'] = sorted(dateinfo.items())
                json_res = json.dumps(res)
                return Response(json_res, HTTP_200_OK)
        except:
            return Response(HTTP_400_BAD_REQUEST)

    def post(self, request, username):
        if not username:
            return Response(HTTP_400_BAD_REQUEST)
        if not request.POST.get('foodname'):
            return Response(status=HTTP_400_BAD_REQUEST)
        try:
            data = DailyUserFood.objects.filter(username=username, food=request.data['foodname'])
            if not data.exists():
                return Response(HTTP_400_BAD_REQUEST)
            else:
                res = dict()
                for row in data:
                    if not row.mealkind in res:
                        res[row.mealkind] = 1
                    else:
                        res[row.mealkind] += 1
                    json_res = json.dumps(res)
                return Response(json_res, HTTP_200_OK)
        except:
            return Response(HTTP_400_BAD_REQUEST)
