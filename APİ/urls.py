from django.urls import path
from APİ.views import *




urlpatterns = [
     path('api/login/', custom_login, name='login-api'),
     path('api/register/', RegisterAPI.as_view(), name='register-api'),
     path("register/",Register, name = "register"),
     path("login/", loggin ,name="login"),
     path("logout/",loggout , name = "logout"),
     path('api/products/', ProductListCreateAPIView.as_view(), name='product-create'),
     path('api/products/<int:id>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
     path('products/admin',  showPrdAll,name="products"),
     path('products/',  showPrd,name="products"),
     path('add/',  add , name ="creatProduct"),
     path('update-permission/<int:id>/', update_permission, name='update-permission'),
     path('bag/',  bag , name ="bag"),

    ]
