from django.utils import timezone
import datetime
from user.forms import AccountForm
from django.http import HttpResponse, Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccountSerializer
from user.models import Account

class AccountList(APIView):
    def get(self, request):
        queryset = Account.objects.all()
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        email = request.data['email']
        print('DEBUG email : ', email)

"""
id 중복 검사 : 
GET /api/account/verify/<str:id>/

email 중복 검사 : 
POST /api/account/verify/
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
        return AccountSerializer(ac).validate_username(username)

    def post(self, request):
        email = request.data['email']
        ac = self.getObject_with_email(email)
        if ac == "OK":
            return Response("사용가능한 이메일입니다.")
        return AccountSerializer(ac).validate_email(email)
