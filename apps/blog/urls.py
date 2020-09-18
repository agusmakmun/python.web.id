# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from updown.views import AddRatingFromModel
from apps.blog.views.post import (
    PostListView, PostListTaggedView,
    PostListAuthorView, PostDetailView
)
from apps.blog.views.tag import TagListView

app_name = 'apps.blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('posts/tagged/<slug:name>/', PostListTaggedView.as_view(), name='post_list_tagged'),
    path('posts/author/<slug:username>/', PostListAuthorView.as_view(), name='post_list_author'),
    path('posts/detail/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/detail/<int:object_id>/rate/<str:score>', AddRatingFromModel(), {
        'app_label': 'blog',
        'model': 'Post',
        'field_name': 'rating'
    }, name='post_rating'),

    path('tags/', TagListView.as_view(), name='tag_list'),
]
