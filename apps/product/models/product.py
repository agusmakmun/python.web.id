# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from apps.blog.models.base import (TimeStampedModel, DefaultManager)
from apps.authuser.models.user import User


class Product(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    image_urls = models.TextField(_('Image URL\s'), blank=True)
    demo_url = models.URLField(_('Demo URL'), null=True, blank=True)
    download_url = models.URLField(_('Download URL'), null=True, blank=True)

    objects = DefaultManager()

    def __str__(self):
        return self.title

    @property
    def list_image_urls(self):
        try:
            return eval(self.image_urls)
        except Exception:
            pass
        return []

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ('-created_at',)
