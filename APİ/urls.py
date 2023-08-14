from APİ.views import *
from APİ.decorator import *
from django.urls import path




urlpatterns = [
     path('bag/', bag , name ="bag"),
     path('add/',  add , name ="add" ),
     path("login/", loggin ,name="login" ),
     path('update/', update , name ="update"),
     path("logout/",loggout , name = "logout"),
     path('products/',  showPrd,name="products"),
     path("register/",Register, name = "register"),
     path("sendEmail/", sendEmailPage ,name = "SendEmail"), 
     path('products/admin',  showPrdAll ,name="products-admin"),
     path("api/all_user/", All_User.as_view() , name="all_user"),
     path('api/login/', custom_login.as_view(), name= 'login-api'),
     path('api/register/', RegisterAPI.as_view(), name='register-api'),
     path("sendEmail/api/sendEmail/", SendEmail.as_view() ,name ="SendEmail"), 
     path("updatePassword/<str:token>/", forgetPassword, name="forgetPassword"),
     path("api/updatePassword/", updataPassword.as_view() ,name = "updataPassword"), 
     path('api/products/', ProductListCreateAPIView.as_view(), name='product-create'),
     path('update_user/', superuser_access_only(UpdateUserAPIView.as_view()), name='update_user'),
     path('update-permission/', admin_access_only(update_permission.as_view()), name= 'update-perm'),
     path('api/products/<int:id>/', admin_access_only(ProductRetrieveUpdateDestroyAPIView), name='product-detail'),

    ]

handler404 = 'APİ.views.No_page'
