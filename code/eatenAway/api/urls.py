from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token, ObtainJSONWebToken
from rest_framework_jwt import authentication
from django.urls import path, include
from . import views

#
# class MyJWTAuthentication(authentication.JSONWebTokenAuthentication):
#     user_model = 'user.Account'
#
#
# obtain_jwt_token = ObtainJSONWebToken.as_view(user_model='user.Account')
#

urlpatterns = [
    path('accounts/', views.AccountList.as_view()),
    path('accounts/login/', views.AccountAuthentication.as_view()),
    path('accounts/verify/', views.verifyExistence.as_view()),
    path('accounts/verify/<str:username>/', views.verifyExistence.as_view()),
    path('activate/<str:uidb64>/<str:token>', views.EmailActivate.as_view(), name='activate'),
    path('token/', obtain_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('token/refresh/', refresh_jwt_token),
]

