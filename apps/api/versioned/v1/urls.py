# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from apps.api.versioned.v1.views.authtoken import (
    LoginView, LogoutView
)

urlpatterns = [
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
]
