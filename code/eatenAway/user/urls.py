from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register('account', views.AccountList)

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('api/', views.AccountList.as_view()),
    path('api/check/username/<str:username>/', views.is_username_exist.as_view()),
    path('api/check/email/<str:email>/', views.is_email_exist.as_view())

    # path('', include(router.urls))
]

