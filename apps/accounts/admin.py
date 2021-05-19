# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from allauth.account.models import (EmailAddress, EmailConfirmation)
from allauth.socialaccount.models import (SocialApp, SocialAccount, SocialToken)
from rest_framework.authtoken.models import Token

from apps.blog.admins.admin import admin_site
from apps.blog.admins.base import DefaultAdminMixin
from apps.accounts.models.user import (User, Profile)


@admin.register(EmailAddress, site=admin_site)
class EmailAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailConfirmation, site=admin_site)
class EmailConfirmationAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialApp, site=admin_site)
class SocialAppAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialAccount, site=admin_site)
class SocialAccountAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialToken, site=admin_site)
class SocialTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(Token, site=admin_site)
class TokenAdmin(admin.ModelAdmin):
    pass


@admin.register(User, site=admin_site)
class UserAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Profile, site=admin_site)
class ProfileAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass
