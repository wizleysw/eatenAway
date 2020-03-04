from django.http import HttpResponse, Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .api.serializers import AccountSerializer
from .models import *


def signup(request):
    return render(request, 'signup.html', {})


class AccountList(APIView):
    def get(self, request):
        queryset = Account.objects.all()
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data)

"""
id 중복 검사 
/user/api/check/id/<str:id>/
"""
class is_username_exist(APIView):
    def get_object(self, username):
        try:
            return Account.objects.get(username=username)
        except Account.DoesNotExist:
            return "OK"

    def get(self, request, username):
        ac = self.get_object(username)
        if ac == "OK":
            return Response("사용가능한 아이디입니다.")
        return AccountSerializer(ac).validate_username(username)

"""
email 중복 검사 
/user/api/check/username/<str:username>/
"""
class is_email_exist(APIView):
    def get_object(self, email):
        try:
            return Account.objects.get(email=email)
        except Account.DoesNotExist:
            return "OK"

    def get(self, request, email):
        ac = self.get_object(email)
        if ac == "OK":
            return Response("사용가능한 이메일입니다.")
        return AccountSerializer(ac).validate_email(email)