# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.db.models import (Q, F, Count)
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView

from apps.product.models.product import Product


class ProductListView(ListView):
    paginate_by = getattr(settings, 'DEFAULT_PAGINATION_NUMBER', 10)
    template_name = 'apps/product/list.html'
    queryset = Product.objects.published()
    context_object_name = 'products'
