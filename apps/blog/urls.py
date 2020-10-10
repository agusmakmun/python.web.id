# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from updown.views import AddRatingFromModel

from apps.blog.models.post import Post
from apps.blog.feed import LatestPosts
from apps.blog.views.page import (
    PageAboutView, PageDevelopersView,
    PageDisclaimerView, PagePrivacyPolicyView,
    PageServicesView, PageSponsorView,
    PageTOSView, ContactUsView
)
from apps.blog.views.post import (
    PostListView, PostListTaggedView,
    PostListAuthorView, PostListAuthorPrivateView,
    PostDetailView, PostCreateView, PostUpdateView,
    PostDeleteJSONView
)
from apps.blog.views.tag import (
    TagListView, TagJSONSearchView,
    TagJSONCreateView
)
from apps.blog.views.addons import FavoriteCreateDeleteJSONView


app_name = 'apps.blog'

info_dict = {
    'queryset': Post.objects.published_public(),
    'date_field': 'updated_at'
}

urlpatterns = [
    # pages
    path('about/', PageAboutView.as_view(), name='page_about'),
    path('developers/', PageDevelopersView.as_view(), name='page_developers'),
    path('disclaimer/', PageDisclaimerView.as_view(), name='page_disclaimer'),
    path('privacy-policy/', PagePrivacyPolicyView.as_view(), name='page_privacy_policy'),
    path('services/', PageServicesView.as_view(), name='page_services'),
    path('sponsor/', PageSponsorView.as_view(), name='page_sponsor'),
    path('terms-of-service/', PageTOSView.as_view(), name='page_terms_of_service'),
    path('contact/', ContactUsView.as_view(), name='page_contact_us'),

    # posts
    path('', PostListView.as_view(), name='post_list'),
    path('posts/me/', PostListAuthorPrivateView.as_view(), name='post_me'),
    path('posts/tagged/<slug:name>/', PostListTaggedView.as_view(), name='post_list_tagged'),
    path('posts/author/<slug:username>/', PostListAuthorView.as_view(), name='post_list_author'),
    path('posts/detail/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/detail/<int:object_id>/rate/<str:score>', AddRatingFromModel(), {
        'app_label': 'blog',
        'model': 'Post',
        'field_name': 'rating'
    }, name='post_rating'),
    path('sitemap.xml', sitemap, {'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.6)}},
         name='django.contrib.sitemaps.views.sitemap'),
    path('posts/feed/', LatestPosts(), name='post_feed'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/update/<slug:slug>/', PostUpdateView.as_view(), name='post_update'),
    path('posts/delete/json/', PostDeleteJSONView.as_view(), name='post_json_delete'),

    # tags
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tags/search/json/', TagJSONSearchView.as_view(), name='tag_json_search'),
    path('tags/create/json/', TagJSONCreateView.as_view(), name='tag_json_create'),

    # addons
    path('favorite/json/', FavoriteCreateDeleteJSONView.as_view(), name='favorite_json_create_delete'),

]
