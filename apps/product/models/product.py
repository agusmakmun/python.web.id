# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from apps.blog.models.base import (TimeStampedModel, DefaultManager)


class Product(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    image_urls = models.TextField(_('Image URL\s'), blank=True)
    demo_url = models.URLField(_('Demo URL'), null=True, blank=True)
    download_url = models.URLField(_('Download URL'), null=True, blank=True)

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
