from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token, ObtainJSONWebToken
from rest_framework_jwt import authentication
from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', views.AccountList.as_view()),
    path('accounts/login/', views.AccountAuthentication.as_view()),
    path('accounts/verify/', views.VerifyExistence.as_view()),
    path('accounts/verify/<str:username>/', views.VerifyExistence.as_view()),
    path('activate/<str:uidb64>/<str:token>', views.EmailActivate.as_view(), name='activate'),

    path('token/', obtain_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('token/refresh/', refresh_jwt_token),

    path('food/', views.FoodList.as_view()),
    path('food/<str:foodname>', views.FoodList.as_view()),
]

