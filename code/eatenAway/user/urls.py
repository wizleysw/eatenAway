from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('intro/', views.RenderIntroPage, name='Intro'),
    path('main/', views.RenderMainPage, name='Main'),
    path('login/', views.RenderLoginPage, name='Login'),
    path('signup/', views.RenderSignupPage, name='Signup'),
    path('waitemailcheck/', views.RenderEmailcheckPage, name='EmailCheck'),
]

