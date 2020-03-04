from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('account/', views.AccountList.as_view()),
    path('username/<str:username>/', views.is_username_exist.as_view()),
    path('email/<str:email>/', views.is_email_exist.as_view()),
]

