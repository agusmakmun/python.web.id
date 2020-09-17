# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from apps.blog.views.post import (
    PostListView, PostListTaggedView,
    PostListAuthorView, PostDetailView
)

app_name = 'apps.blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('posts/tagged/<slug:slug>/', PostListTaggedView.as_view(), name='post_list_tagged'),
    path('posts/author/<slug:username>/', PostListAuthorView.as_view(), name='post_list_author'),
    path('posts/detail/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
