# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProductConfig(AppConfig):
    name = 'apps.product'
    verbose_name = _('App Product')
    DEFAULT_AUTO_FIELD = settings.DEFAULT_AUTO_FIELD
