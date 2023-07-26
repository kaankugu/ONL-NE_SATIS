
from django.contrib import admin
from django.urls import path , include
from APİ.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import re_path


urlpatterns = [
    path('', HomePage , name="home-page" ),
    path('admin/', admin.site.urls),
    path('', include("APİ.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
