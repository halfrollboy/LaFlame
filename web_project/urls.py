"""
    Этот код тянет ссылается на hello/urls.py django.urls.include, 
    в котором сохраняются маршруты приоложения, содержащиеся в приложении. Это разделение полезно
    когда проект содержит несколько приложений
"""

from django.contrib import admin
from django.urls import include, path 
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from django.conf import settings

#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("flesh.urls")),
    path('main_cabinet/', include("cabinet.urls", namespace='main_cab')),
    path('blog/',include("blog.urls",namespace='blog')),
    path('captcha/', include('captcha.urls')), #модуль с каптчей его не видно в основных приложения 
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

