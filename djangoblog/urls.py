"""djangoblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog
from django.conf import settings

urlpatterns = [
    # internationalization
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),

    path('martor/', include('martor.urls')),
    path('accounts/', include('allauth.urls')),

    path('', include('app_blog.urls')),
    path('', include('app_user.urls')),
    path('dashboard/', include('app_dashboard.urls')),

    #path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/', include('app_api.urls')),
]

if settings.DEBUG:
    urlpatterns += [path('admin/', admin.site.urls)]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    handler400 = 'djangoblog.utils.handler.handler400'
    handler403 = 'djangoblog.utils.handler.handler403'
    handler404 = 'djangoblog.utils.handler.handler404'
    handler500 = 'djangoblog.utils.handler.handler500'
