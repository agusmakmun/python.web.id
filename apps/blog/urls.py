# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from apps.blog.views.post import (PostListView, PostListTaggedView)

app_name = 'apps.blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('posts/tagged/<slug:slug>/', PostListTaggedView.as_view(), name='post_list_tagged'),
]
