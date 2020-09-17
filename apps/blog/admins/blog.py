# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.blog.models.tag import Tag
from apps.blog.models.post import (Post, Page)
from apps.blog.models.addons import (Visitor, Favorite, Gallery)
from apps.blog.admins.base import DefaultAdminMixin
from apps.blog.admins.admin import admin_site


@admin.register(Tag, site=admin_site)
class TagAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Post, site=admin_site)
class PostAdmin(DefaultAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


@admin.register(Page, site=admin_site)
class PageAdmin(DefaultAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


@admin.register(Visitor, site=admin_site)
class VisitorAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Favorite, site=admin_site)
class FavoriteAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Gallery, site=admin_site)
class GalleryAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass
