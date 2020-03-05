import urllib
import json
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from user.forms import AccountForm
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccountSerializer
from user.models import Account
from eatenAway.settings import GOOGLE_RECAPTCHA_SECRET_KEY


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
            cl = verifyExistence();
            ac = verifyExistence.getObject_with_username(cl, form_data.cleaned_data['username'])
            if not AccountSerializer(ac).validate_username(form_data.cleaned_data['username']):
                return Response('fail.', status=HTTP_400_BAD_REQUEST)

            ac = verifyExistence.getObject_with_email(cl, form_data.cleaned_data['email'])
            if not AccountSerializer(ac).validate_email(form_data.cleaned_data['email']):
                return Response('fail.', status=HTTP_400_BAD_REQUEST)

            new_account = form_data.save(commit=False)
            new_account.set_password(form_data.cleaned_data['password'])
            new_account.save()
            return Response('success.', status=HTTP_201_CREATED)

        else:
            return Response('fail.', status=HTTP_400_BAD_REQUEST)

"""
id 중복 검사 : 
GET /api/accounts/verify/<str:id>/

email 중복 검사 : 
POST /api/accounts/verify/
"""
class verifyExistence(APIView):
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
