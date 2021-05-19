# -*- coding: utf-8 -*-

from apps.blog.admins import (
    admin, DefaultAdminMixin,
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
