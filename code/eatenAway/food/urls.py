from django.urls import path, include
from . import views

urlpatterns = [
    path('menu/<str:foodname>', views.menuDetail, name='menu'),
    path('addmenu/', views.addMenu, name='addmenu'),
    path('checkdatemenu/', views.checkDateMenu, name='checkdatemenu'),
    path('updatedatemenu/', views.updateDateMenu, name='updatedatemneu'),
]

