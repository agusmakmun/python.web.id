# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from apps.blog.models.base import (TimeStampedModel, DefaultManager)


class Tag(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    name = models.SlugField(_('Name'), max_length=200, unique=True)
    description = models.TextField(_('Description'), blank=True)

    objects = DefaultManager()

    def __str__(self):
        return self.name

    def get_posts(self):
        if hasattr(self, 'post_set'):
            return self.post_set.published_public()
        return None

    @property
    def total_posts(self):
        posts = self.get_posts()
        return posts.count() if posts else 0

    def save(self, *args, **kwargs):

        # save that name is as a slug type
        self.name = slugify(self.name)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ('-created_at',)
