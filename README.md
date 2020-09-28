# Eaten Away

Django service website to manage food experience.
(Images from Spirited-Away is used)

## Features

- SignIn/SignUp
- Google Recaptcha
- Email Verification
- Food Menu Recommendation
- Food Menu History Of User
- Map of Store Info(Kakao Api)
- Simple Food Pattern Analytics using Google Map

## Dev note

Dev details are written in Korean. 

https://bughunting.kr/dev/Django-+-REST-+-SQLite-@-docker%EB%A1%9C-Eaten_Away-%EC%84%9C%EB%B9%84%EC%8A%A4-%EA%B0%9C%EB%B0%9C%ED%95%98%EA%B8%B0/

## Objectives

This project is aimed to learn these things.

- Django : Learn MVT pattern
- REST : Stateless Server to communicate with
- JWT : Use Token instead Session
- Recaptcha : D-DOS, Brute Force prevention

## Dependencies

```
root@b099b068dc26:/code# pip list
Package                 Version
----------------------- -------
asgiref                 3.2.3
attrs                   19.3.0
coverage                5.0.3
Django                  3.0.3
django-cors-headers     3.2.1
django-rest-auth        0.9.5
django-rest-authtoken   1.2.4
djangorestframework     3.11.0
djangorestframework-jwt 1.11.0
more-itertools          8.2.0
packaging               20.1
pip                     20.0.2
pluggy                  0.13.1
py                      1.8.1
PyJWT                   1.7.1
pyparsing               2.4.6
pytest                  5.3.5
pytest-cov              2.8.1
pytz                    2019.3
setuptools              45.1.0
six                     1.14.0
sqlparse                0.3.0
wcwidth                 0.1.8
wheel                   0.34.2
```

## How To Use ?

code directiory contains Django server written in Python. api directory is for REST api, eatenAway, food is for Django.

You can add FoodList using bulk.py inside code/eatenAway. I have also added Dockerfile to easy build and run Django server.

For better security, you should change SECRET_KEY used in settings.py. If you don't have Google Recaptcha secret key, disable features. 

### REST API

```python
""" 
GET : /api/accounts/verify/<str:id>/
용도 : 아이디에 대한 값이 이미 존재하는지 여부를 리턴
POST : /api/accounts/verify/
용도 : 이메일에 대한 값이 이미 존재하는지 여부를 리턴
"""
class APIForNewAccountCheck(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username):
        AccountInfo = UserAccount(username, None)
        if AccountInfo.already_have_username():
            return Response("이미 사용중인 아이디입니다.", status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_200_OK)

    def post(self, request):
        AccountInfo = UserAccount(None, None)
        email = request.data['email']
        if AccountInfo.already_have_email(email):
            return Response("이미 사용중인 아이디입니다.", status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_200_OK)
```

I have commented usage of REST api. Some of API needs jwt token permission. You can find code in here.

https://github.com/wizleysw/eatenAway/blob/master/code/eatenAway/api/views.py

## Shape

- Api

![Api](https://raw.githubusercontent.com/wizleysw/wizleysw.github.io/master/_posts/img/eatenAway/queryset.png)

- Food Pattern

![Food Pattern](https://raw.githubusercontent.com/wizleysw/wizleysw.github.io/master/_posts/img/eatenAway/graph_food.png)

- Food Ring Pattern

![Food Ring Pattern](https://raw.githubusercontent.com/wizleysw/wizleysw.github.io/master/_posts/img/eatenAway/porklet_graph.png)

- Map

![Map](https://raw.githubusercontent.com/wizleysw/wizleysw.github.io/master/_posts/img/eatenAway/foodmap.png)

