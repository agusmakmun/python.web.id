# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from app_blog.views.post import PostListView

app_name = 'app_blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
]
