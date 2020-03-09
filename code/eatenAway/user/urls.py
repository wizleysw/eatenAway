from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('main/', views.mainPage, name='main'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('waitemailcheck/', views.waitemailcheck, name='waitemailcheck'),
]

