from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('emailverify/', views.emailverify, name='emailverify'),
]

