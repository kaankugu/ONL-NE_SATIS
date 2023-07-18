
from django.contrib import admin
from django.urls import path , include
from APİ.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', HomePage , name="home-page" ),
    path('admin/', admin.site.urls),
    path('', include("APİ.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

