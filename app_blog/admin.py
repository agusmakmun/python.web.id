# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf import settings

from updown.models import Vote
from app_blog.models import *


class TagAdmin(admin.ModelAdmin):
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_display = ['title', 'total_posts', 'created', 'modified']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['created', 'modified']
    search_fields = ['title', 'slug']


class PostAdmin(admin.ModelAdmin):
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_display = ['title', 'author', 'rating_likes', 'total_visitors',
                    'total_favorites', 'is_featured',  'publish']
    search_fields = ['title', 'slug', 'description', 'author__username',
                     'keywords', 'meta_description']
    list_filter = ['publish', 'is_featured', 'created', 'modified']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']


class PageAdmin(admin.ModelAdmin):
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_display = ['title', 'author', 'status', 'created', 'modified']
    search_fields = ['title', 'slug', 'status', 'author__username']
    list_filter = ['publish', 'status', 'created', 'modified']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']


class VisitorAdmin(admin.ModelAdmin):
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_display = ['post', 'ip', 'created']
    list_filter = ['created', 'modified']
    search_fields = ['post__title', 'ip']
    raw_id_fields = ['post']


class FavoriteAdmin(admin.ModelAdmin):
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_display = ['post', 'user', 'created']
    list_filter = ['created', 'modified']
    search_fields = ['post__title', 'user__username']
    raw_id_fields = ['user', 'post']


class GalleryAdmin(admin.ModelAdmin):
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_display = ['__str__', 'author', 'attachment', 'created']
    list_filter = ['created', 'modified']
    search_fields = ['title', 'author__username']
    raw_id_fields = ['author']


class VoteAdmin(admin.ModelAdmin):
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_display = ['content_object', 'score', 'user',
                    'ip_address', 'date_added', 'date_changed']
    list_filter = ['score', 'date_added', 'date_changed']
    search_fields = ['user__username', 'ip_address', 'score']
    raw_id_fields = ['user']

admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Vote, VoteAdmin)
