# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import (path, re_path)
from django.views.generic import TemplateView
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from updown.views import AddRatingFromModel
from app_blog.feed import LatestPosts
from app_blog.views import *

info_dict = {
    'queryset': Post.objects.published(),
    'date_field': 'modified',
}

urlpatterns = [
    path('', PostList.as_view(), name='posts_list'),
    path('search/', PostList.as_view(), name='posts_search'),
    path('posts/detail/<slug:slug>/', PostDetail.as_view(), name='posts_detail'),
    path('posts/tagged/<slug:slug>/', PostTagged.as_view(), name='posts_tagged'),
    # path('posts/author/<slug:username>/', PostAuthor.as_view(), name='posts_author'),
    re_path(r'^posts/author/(?P<username>.*)/$', PostAuthor.as_view(), name='posts_author'),
    path('posts/me/', PostAuthorPrivate.as_view(), name='posts_me'),

    # updown url
    path('rating/<int:object_id>/rate/<slug:score>', AddRatingFromModel(),
         {'app_label': 'app_blog', 'model': 'Post', 'field_name': 'rating'}, name='posts_vote_rating'),

    path('posts/create/', PostCreate.as_view(), name='posts_create'),
    path('posts/edit/<slug:slug>/', PostEdit.as_view(), name='posts_edit'),
    path('posts/delete/<int:pk>/', PostDeleteJSON.as_view(), name='posts_delete'),

    path('tags/', TagList.as_view(), name='tags_list'),
    #path('tags/create/', TagCreate.as_view(), name='tags_create'),
    path('tags/create/json/', TagCreateJSON.as_view(), name='tags_create_json'),
    path('tags/search/json/', TagSearchJSON.as_view(), name='tags_search_json'),

    path('posts/featured/<int:pk>/mark/', MarkAsFeaturedJSON.as_view(), name='posts_mark_as_featured'),
    path('favorite/crud/<int:pk>/', FavoriteCrudJSON.as_view(), name='favorite_crud'),
    path('vote/delete/<int:post_id>/<int:user_id>/<slug:status>/',
         VoteDeleteJSON.as_view(), name='vote_delete'),

    path('pages/create/', PageCreate.as_view(), name='pages_create'),
    path('pages/edit/<slug:slug>/', PageEdit.as_view(), name='pages_edit'),
    path('pages/delete/<int:pk>/', PageDeleteJSON.as_view(), name='pages_delete'),
    path('pages/<slug:slug>/', PageDetail.as_view(), name='pages_detail'),
    path('contact/', ContactUs.as_view(), name='contact_us'),

    path('feed/', LatestPosts(), name='feed'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': {'blog': GenericSitemap(
        info_dict, priority=0.6)}}, name='django.contrib.sitemaps.views.sitemap'),
]
