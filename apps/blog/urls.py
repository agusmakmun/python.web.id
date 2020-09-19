# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from updown.views import AddRatingFromModel
from apps.blog.views.post import (
    PostListView, PostListTaggedView,
    PostListAuthorView, PostDetailView
)
from apps.blog.views.tag import TagListView
from apps.blog.views.page import (
    PageAboutView, PageDisclaimerView,
    PagePrivacyPolicyView, PageServicesView,
    PageTOSView
)

app_name = 'apps.blog'

urlpatterns = [
    # posts
    path('', PostListView.as_view(), name='post_list'),
    path('posts/tagged/<slug:name>/', PostListTaggedView.as_view(), name='post_list_tagged'),
    path('posts/author/<slug:username>/', PostListAuthorView.as_view(), name='post_list_author'),
    path('posts/detail/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/detail/<int:object_id>/rate/<str:score>', AddRatingFromModel(), {
        'app_label': 'blog',
        'model': 'Post',
        'field_name': 'rating'
    }, name='post_rating'),

    # tags
    path('tags/', TagListView.as_view(), name='tag_list'),

    # pages
    path('about/', PageAboutView.as_view(), name='page_about'),
    path('disclaimer/', PageDisclaimerView.as_view(), name='page_disclaimer'),
    path('privacy-policy/', PagePrivacyPolicyView.as_view(), name='page_privacy_policy'),
    path('services/', PageServicesView.as_view(), name='page_services'),
    path('terms-of-service/', PageTOSView.as_view(), name='page_terms_of_service'),
]
