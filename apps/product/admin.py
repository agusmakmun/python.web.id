# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.blog.admins.admin import admin_site
from apps.blog.admins.base import DefaultAdminMixin
from apps.product.models.ads import Advertisement
from apps.product.models.product import Product


@admin.register(Advertisement, site=admin_site)
class AdvertisementAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Product, site=admin_site)
class ProductAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass
