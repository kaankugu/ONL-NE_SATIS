from django.urls import path
from APİ.views import *
from APİ.decorator import *




urlpatterns = [
     path('bag/', bag , name ="bag"),
     path("login/", loggin ,name="login" ),
     path('update/', update , name ="update"),
     path("logout/",loggout , name = "logout"),
     path('add/',  add , name ="add" ),
     path('products/',  showPrd,name="products"),
     path("register/",Register, name = "register"),
     path('products/admin',  showPrdAll,name="products-admin"),
     path("api/all_user/", All_User.as_view() , name= "all_user"),
     path('api/login/', custom_login.as_view(), name= 'login-api'),
     path('api/register/', RegisterAPI.as_view(), name='register-api'),
     path('update-permission/', update_permission.as_view(), name= 'update-perm'),
     path('update_user/', superuser_access_only(UpdateUserAPIView.as_view()), name='update_user'),
     path('api/products/', ProductListCreateAPIView.as_view(), name='product-create'),
     path('api/products/<int:id>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
     path("sendEmail/api/sendEmail/", SendEmail.as_view() ,name = "SendEmail"), 
     path("sendEmail/", sendEmailPage ,name = "SendEmail"), 
     path("updatePassword/<str:token>/", forgetPassword, name="forgetPassword"),
     path("api/updatePassword/", updataPassword.as_view() ,name = "updataPassword"), 

    ]

handler404 = 'APİ.views.No_page'
