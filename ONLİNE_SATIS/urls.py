
from django.contrib import admin
from django.urls import path , include
from APİ.views import *

urlpatterns = [
    path('', HomePage , name="home-page" ),
    path('admin/', admin.site.urls),
    path('', include("APİ.urls")),
]
