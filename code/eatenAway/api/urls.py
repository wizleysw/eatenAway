from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', views.AccountList.as_view()),
    path('accounts/verify/', views.verifyExistence.as_view()),
    path('accounts/verify/<str:username>/', views.verifyExistence.as_view()),
]

