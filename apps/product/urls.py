# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from apps.product.views.product import ProductListView

app_name = 'apps.product'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
]
