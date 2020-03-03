from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.getuser, name='getuser'),
    path('signup/', views.signup, name='signup'),
]

