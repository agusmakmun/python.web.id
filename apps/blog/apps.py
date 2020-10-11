# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BlogConfig(AppConfig):
    name = 'apps.blog'
    verbose_name = _('App Blog')
