# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from apps.dashboard.views.index import DashboardIndexView

app_name = 'apps.dashboard'

urlpatterns = [
    path('', DashboardIndexView.as_view(), name='dashboard_index'),
]
