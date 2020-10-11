# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from apps.api.versioned.v1.views.authtoken import (LoginView, LogoutView, UserDetailsView)
from apps.api.versioned.v1.views.tag import TagView
from apps.api.versioned.v1.views.post import PostView


urlpatterns = [
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/user/', UserDetailsView.as_view()),

    path('tag/', TagView.as_view()),
    path('post/', PostView.as_view()),
]
