# -*- coding: utf-8 -*-

from .admin import admin
from .base import DefaultAdminMixin
from .blog import (
    TagAdmin, PostAdmin, PageAdmin,
    VisitorAdmin, FavoriteAdmin, GalleryAdmin
)

__all__ = (
    'admin',
    'DefaultAdminMixin',

    'TagAdmin',
    'PostAdmin',
    'PageAdmin',
    'VisitorAdmin',
    'FavoriteAdmin',
    'GalleryAdmin'
)
