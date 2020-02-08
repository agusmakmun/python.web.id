# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import (path, re_path)

from app_user.views import *

urlpatterns = [
    path('users/', UserList.as_view(), name='users_list'),
    path('accounts/profile/', ProfileEdit.as_view(), name='profile_edit'),
    # path('accounts/profile/<slug:username>/', ProfileDetail.as_view(), name='profile_detail'),
    # path('accounts/profile/<slug:username>/activity/', ProfileDetailActivity.as_view(), name='profile_activity'),

    re_path(r'^accounts/profile/activity/(?P<username>.*)/$', ProfileDetailActivity.as_view(), name='profile_activity'),
    re_path(r'^accounts/profile/(?P<username>.*)/$', ProfileDetail.as_view(), name='profile_detail'),
]
