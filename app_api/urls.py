# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import (path, re_path)

from rest_framework.authtoken.views import obtain_auth_token

from app_api.views.docs import *
from app_api.views.api import *


urlpatterns = [
    path('auth', AuthView.as_view(), name='api_check_token_auth'),
    path('login', obtain_auth_token, name='api_login'),
    path('logout', api_logout, name='api_logout'),

    path('tags', TagListView.as_view(), name='api_tags'),
    path('tags/detail/<slug:slug>', TagDetailView.as_view(), name='api_tags_detail'),

    path('posts', PostListView.as_view(), name='api_posts'),
    path('posts/detail/<slug:slug>', PostDetailView.as_view(), name='api_posts_detail'),
    path('posts/tagged/<slug:slug>', PostTaggedListView.as_view(), name='api_posts_tagged'),
    # path('posts/author/<slug:username>', PostAuthorListView.as_view(), name='api_posts_author'),
    re_path(r'^posts/author/(?P<username>.*)$', PostAuthorListView.as_view(), name='api_posts_author'),

    path('users', UserProfileListView.as_view(), name='api_users'),
    # path('users/detail/<slug:username>', UserProfileDetailView.as_view(), name='api_users_detail'),
    re_path(r'^users/detail/(?P<username>.*)$', UserProfileDetailView.as_view(), name='api_users_detail'),

    # api docs
    path('docs/', DocumentationHome.as_view(), name='docs_home'),
    path('docs/<slug:slug>/', DocumentationDetail.as_view(), name='docs_detail'),
]
