from django.urls import path
from APİ.views import *




urlpatterns = [
     path('api/login/', CustomLoginView.as_view(), name='login-api'),
     path('api/register/', RegisterAPI.as_view(), name='register-api'),
     path("register/",Register, name = "register"),
     path("loggin/", loggin ,name="login"),
    ]
