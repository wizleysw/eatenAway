from django.urls import path, include
from . import views

urlpatterns = [
    path('menu/<str:foodname>', views.menuDetail, name='menu'),
]

