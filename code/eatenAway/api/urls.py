from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from django.urls import path
from . import views

urlpatterns = [
    path('accounts/', views.APIForAccountRegistration.as_view()),
    path('accounts/profile/<str:username>', views.APIForAccountProfile.as_view()),
    path('accounts/login/', views.APIForAccountAuthentication.as_view()),
    path('accounts/verify/', views.APIForNewAccountCheck.as_view()),
    path('accounts/verify/<str:username>/', views.APIForNewAccountCheck.as_view()),
    path('activate/<str:uidb64>/<str:token>', views.APIForEmailActivation.as_view()),

    path('token/', obtain_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('token/refresh/', refresh_jwt_token),

    path('food/', views.APIForFoodDetail.as_view()),
    path('food/<str:foodname>', views.APIForFoodDetail.as_view()),
    path('food/user/<str:username>', views.APIForUserFoodDetail.as_view()),
    path('food/preference/<str:username>', views.APIForUserFoodChoice.as_view()),
    # path('food/<str:foodname>/comment', views.APIForFoodComment.as_view()),

    path('food/date/<str:username>/<str:date>', views.APIForUserFoodDetailByDate.as_view()),
    path('food/date/<str:username>', views.APIForUserFoodDetailByDate.as_view()),
    path('food/date/<str:username>/<str:date>/<str:mealkind>', views.APIForUserFoodDetailByDate.as_view()),

]

