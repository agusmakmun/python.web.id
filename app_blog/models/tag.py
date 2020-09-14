# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from app_blog.models.base import (TimeStampedModel, DefaultManager)
from app_blog.utils.slug import generate_unique_slug


class Tag(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)

    objects = DefaultManager()

    def __str__(self):
        return self.title

    def get_posts(self):
        if hasattr(self, 'postset'):
            return self.postset.published()
        return None

    @property
    def total_posts(self):
        posts = self.get_posts()
        return posts.count() if posts else 0

    def save(self, *args, **kwargs):
        if not self.pk:
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Post, self.title)
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ('-created_at',)
