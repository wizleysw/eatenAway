from django.urls import path
from . import views

urlpatterns = [
    path('menu/<str:foodname>', views.RenderFoodPage, name='Food'),
    path('addmenu/', views.RenderAddMenuPage, name='AddMenu'),
    path('checkdatemenu/', views.RenderCheckMenuByDatePage, name='CheckMenuByDate'),
    path('updatedatemenu/', views.RenderUpdateMenuByDatePage, name='UpdateMenuByDate'),
]

