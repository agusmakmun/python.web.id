# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from apps.accounts.views.profile import (
    ProfileUpdateView,
    ProfileDetailView,
    ProfileDetailActivityView
)

app_name = 'apps.accounts'

urlpatterns = [
    path('accounts/profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('accounts/profile/activity/<slug:username>/',
         ProfileDetailActivityView.as_view(), name='profile_activity'),
    path('accounts/profile/<slug:username>/', ProfileDetailView.as_view(), name='profile_detail'),
]
