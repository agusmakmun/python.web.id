# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.blog.models.base import (TimeStampedModel, DefaultManager)


class Advertisement(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)

    class PlaceOptions(models.TextChoices):
        navbar_top = 'navbar_top', _('Navbar (Top)')

        post_list_top = 'post_list_top', _('Post List (Top)')
        post_list_middle = 'post_list_middle', _('Post List (Middle)')
        post_list_bottom = 'post_list_bottom', _('Post List (Bottom)')

        post_detail_top = 'post_detail_top', _('Post Detail (Top)')
        post_detail_middle = 'post_detail_middle', _('Post Detail (Middle)')
        post_detail_bottom = 'post_detail_bottom', _('Post Detail (Bottom)')

        sidebar_top = 'sidebar_top', _('Sidebar (Top)')
        sidebar_middle = 'sidebar_middle', _('Sidebar (Middle)')
        sidebar_bottom = 'sidebar_bottom', _('Sidebar (Bottom)')

        footer = 'footer', _('Footer')

    place = models.CharField(_('Jenis'), max_length=20, unique=True,
                             choices=PlaceOptions.choices,
                             default=PlaceOptions.navbar_top)

    raw_html = models.TextField(_('Raw HTML'),
                                help_text=_('Please do not use javascript syntax.'))

    objects = DefaultManager()

    def __str__(self):
        return self.place

    class Meta:
        verbose_name = _('Advertisement')
        verbose_name_plural = _('Advertisements')
        ordering = ('-created_at',)
