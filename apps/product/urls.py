# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from apps.product.views.product import (
    ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateView,
    ProductListAuthorPrivateView, ProductDeleteJSONView
)

app_name = 'apps.product'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/me/', ProductListAuthorPrivateView.as_view(), name='product_me'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/delete/json/', ProductDeleteJSONView.as_view(), name='product_json_delete'),
    path('products/update/<int:id>/', ProductUpdateView.as_view(), name='product_update'),
    path('products/detail/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
]
