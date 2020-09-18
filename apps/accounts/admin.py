# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.blog.admins.admin import admin_site
from apps.blog.admins.base import DefaultAdminMixin
from apps.accounts.models.user import (User, Profile)


@admin.register(User, site=admin_site)
class UserAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Profile, site=admin_site)
class ProfileAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass
