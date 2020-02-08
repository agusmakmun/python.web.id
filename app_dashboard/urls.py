# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from app_dashboard.views import *

urlpatterns = [
    path('', DashboardHome.as_view(), name='dashboard_home'),
    path('posts/', DashboardPosts.as_view(), name='dashboard_posts'),
    path('tags/', DashboardTags.as_view(), name='dashboard_tags'),
    path('users/', DashboardUsers.as_view(), name='dashboard_users'),
    path('users/deactivate/<int:pk>/', DashboardUserActivationJSON.as_view(),
         name='dashboard_users_activation'),
    path('users/delete/<int:pk>/', DashboardUserDeleteJSON.as_view(), name='dashboard_users_delete'),
    path('pages/', DashboardPages.as_view(), name='dashboard_pages'),
    path('galleries/', DashboardGalleries.as_view(), name='dashboard_galleries'),
    path('galleries/create/', DashboardGalleryCreate.as_view(), name='dashboard_galleries_create'),
    path('galleries/edit/<int:pk>/', DashboardGalleryEdit.as_view(), name='dashboard_galleries_edit'),
    path('galleries/delete/<int:pk>/', DashboardGalleryDeleteJSON.as_view(),
         name='dashboard_galleries_delete'),
    path('visitors/', DashboardVisitors.as_view(), name='dashboard_visitors'),
    path('visitors/delete/<int:pk>/', DashboardVisitorDeleteJSON.as_view(),
         name='dashboard_visitors_delete'),
]
