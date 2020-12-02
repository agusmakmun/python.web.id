"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import (path, include)
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('martor/', include('martor.urls')),

    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),

    path('accounts/', include('allauth.urls')),
    path('', include('apps.accounts.urls')),
    path('', include('apps.blog.urls')),
    path('', include('apps.product.urls')),
    path('api/', include('apps.api.urls')),
    path('dash/', include('apps.dashboard.urls')),
]

if settings.DEBUG:
    handler400 = 'core.utils.handler.handler400'
    handler403 = 'core.utils.handler.handler403'
else:
    handler400 = 'core.utils.handler.handler400'
    handler403 = 'core.utils.handler.handler403'
    handler404 = 'core.utils.handler.handler404'
    handler500 = 'core.utils.handler.handler500'
