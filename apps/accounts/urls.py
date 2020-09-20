# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from apps.accounts.views.profile import ProfileDetailView

app_name = 'apps.accounts'

urlpatterns = [
    path('accounts/profile/<slug:username>/', ProfileDetailView.as_view(), name='profile_detail'),
]
