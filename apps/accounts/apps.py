# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountsConfig(AppConfig):
    name = 'apps.accounts'
    verbose_name = _('App Auth User')
    default_auto_field = settings.DEFAULT_AUTO_FIELD
