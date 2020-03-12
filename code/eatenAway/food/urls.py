from django.urls import path, include
from . import views

urlpatterns = [
    path('test/',  views.testPage, name='test'),
    path('menu/<str:foodname>', views.testPage, name='menu'),
]

