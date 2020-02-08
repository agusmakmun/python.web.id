# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf import settings

from app_user.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_display = ['user', 'display_name', 'location', 'website', 'birth_date']
    search_fields = ['user__username', 'display_name', 'about_me',
                     'website', 'twitter', 'linkedin', 'github']
    raw_id_fields = ['user']

admin.site.register(Profile, ProfileAdmin)
