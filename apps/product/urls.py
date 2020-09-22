# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from apps.product.views.product import (
    ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateView
)

app_name = 'apps.product'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/d/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/update/<int:id>/', ProductUpdateView.as_view(), name='product_update'),
]
