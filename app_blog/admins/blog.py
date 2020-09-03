# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from app_blog.models.tag import Tag
from app_blog.models.post import (Post, Page)
from app_blog.models.addons import (Visitor, Favorite, Gallery)
from app_blog.admins.base import DefaultAdminMixin
from app_blog.admins.admin import admin_site


@admin.register(Tag, site=admin_site)
class TagAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Post, site=admin_site)
class PostAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Page, site=admin_site)
class PageAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Visitor, site=admin_site)
class VisitorAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Favorite, site=admin_site)
class FavoriteAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Gallery, site=admin_site)
class GalleryAdmin(DefaultAdminMixin, admin.ModelAdmin):
    pass
