from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.forms import AccountForm
from django.http import Http404, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccountSerializer, CommentSerializer, AccountProfileSerializer
from user.models import Account
from food.models import Food, DailyUserFood, FoodComment
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
import operator

from user.tokens import Token
from .recaptchas import is_recaptcha_correct
from .accounts import UserAccount
from .foods import DailyFood, Food

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
    permission_classes = (AllowAny,)

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
GET : user/apis.py -> get_user_profile (/api/accounts/profile/<str:username>)
용도  : 토큰의 사용자 아이디 정보로 프로파일 정보 가져옴
"""
class AccountProfile(APIView):
    # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = AccountProfileSerializer

    def get(self, request, username):
        AccountInfo = UserAccount(username, None)
        if AccountInfo.is_account_available():
            serialized = AccountProfileSerializer(AccountInfo.account)
            return Response(serialized.data, HTTP_200_OK)
        else:
            return Response(HTTP_400_BAD_REQUEST)


"""
id 중복 검사 : 
GET /api/accounts/verify/<str:id>/

email 중복 검사 : 
POST /api/accounts/verify/
"""
class VerifyExistence(APIView):
    permission_classes = (AllowAny,)

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
POST : user/apis.py -> get_user_token (/api/accounts/login/)
용도  : 사용자 아이디 패스워드 검증 후 token 발급 
"""
class AccountAuthentication(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        if not is_recaptcha_correct(request.data['g-recaptcha-response']):
            return Response("FAIL.", status=HTTP_400_BAD_REQUEST)

        username = request.data['username']
        password = request.data['password']
        AccountInfo = UserAccount(username, password)
        if AccountInfo.is_password_correct():
            tk = Token(None)
            token = tk.get_account_token(username, password)
            if token is not None:
                return Response({'token': token}, status=HTTP_200_OK)
            else:
                return Response(status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


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
GET : user/apis.py -> get_user_foodcount (/api/food/user/<str:username>)
용도  : 특정 기간내에 특정 음식을 몇 번 먹었는지 정보 가져옴

POST : food/apis.py -> get_user_food (/api/food/user/<str:username>) with post_data['foodname']
용도 : 특정 음식을 아침/점심/저녁에 각각 몇 번 먹었는지에 대한 정보 가져옴
"""
class UserDailyFoodList(APIView):
    # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, username):
        if not username:
            return Response(HTTP_400_BAD_REQUEST)

        UserFood = DailyFood(username)
        foodlist = UserFood.get_user_food_with_day(9)

        if not foodlist.exists():
            return Response(HTTP_400_BAD_REQUEST)

        else:
            res = UserFood.get_foodcount_with_date()
            return Response(res, HTTP_200_OK)

    def post(self, request, username):
        if not username:
            return Response(HTTP_400_BAD_REQUEST)
        if not request.POST.get('foodname'):
            return Response(HTTP_400_BAD_REQUEST)

        UserFood = DailyFood(username)
        foodlist = UserFood.get_user_food(request.data['foodname'])

        if not foodlist.exists():
            return Response(HTTP_400_BAD_REQUEST)

        else:
            res = UserFood.get_user_food_mealkind()
            return Response(res, HTTP_200_OK)


"""
GET : user/apis.py -> get_user_preference (/api/food/preference/<str:username>)
용도  : 특정 기간 내의 사용자의 음식 리스트를 조회하여 추천 메뉴 7개를 선정함
"""
class UserFoodPreferenceList(APIView):
    # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, username):
        UserFood = DailyFood(username)
        foodlist = UserFood.get_user_food_with_day(9)

        if not foodlist.exists():
            return Response(HTTP_400_BAD_REQUEST)

        else:
            res = UserFood.get_preference()
            return Response(res, HTTP_200_OK)


'''
get : 특정 일자의 유저의 아침/점심/저녁 리스트 리턴
post : 특정 일자의 아침/점심/저녁 정보 추가 또는 업데이트 및 삭제
'''
class UserFoodByDate(APIView):
    # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, username, date):
        data = DailyUserFood.objects.filter(username=username, date=date)
        res = {}
        res['B'] = res['L'] = res['D'] = '-'
        if not data.exists():
            return Response(res, HTTP_400_BAD_REQUEST)
        else:
            for row in data:
                res[row.mealkind] = row.food
            return Response(res, HTTP_200_OK)


    def post(self, request, username):
        try:
            date = request.data['date']
            mealkind = request.data['mealkind']
            foodname = request.data['foodname']
            food_data = Food.objects.get(menuname=foodname)
            mealkind_choice = ['B', 'L', 'D']
            if not mealkind in mealkind_choice:
                return Response(HTTP_400_BAD_REQUEST)
        except:
            return Response(HTTP_400_BAD_REQUEST)
        try:
            data = DailyUserFood.objects.get(username=username, date=date, mealkind=mealkind)
            data.food = foodname
            data.save()
            return Response(HTTP_201_CREATED)

        except DailyUserFood.DoesNotExist:
            data = DailyUserFood(username=username, food=foodname, mealkind=mealkind, date=date)
            data.save()
            return Response(HTTP_201_CREATED)


    def delete(self, request, username, date, mealkind):
        try:
            data = DailyUserFood.objects.get(username=username, date=date, mealkind=mealkind)
            data.delete()
            return Response(HTTP_200_OK)
        except:
            return Response(HTTP_400_BAD_REQUEST)

'''
get : 음식에 대한 List 

'''
class FoodCommentList(APIView):
    # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = CommentSerializer

    def get(self, request, foodname):
        food = Food.objects.get(menuname=foodname)
        data = FoodComment.objects.select_related('food').filter(food=food, parent=None)

        # serialized = self.get_serializer(data, many=True)
        serialized = CommentSerializer(data, many=True)

        # for row in data:
        #     print(row)
        # FoodComment.objects.filter(food=food)
        return Response(serialized.data, HTTP_200_OK)