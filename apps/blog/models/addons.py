# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.blog.models.base import (TimeStampedModel, DefaultManager)
from apps.blog.models.post import Post
from apps.accounts.models.user import User


class Visitor(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    headers = models.TextField(_('Headers'), null=True, blank=True)
    ip_address = models.CharField(_('IP Address'), max_length=40)
    slug_url = models.TextField(_('Slug URL'))

    objects = DefaultManager()

    def __str__(self):
        message = _('%(ip_address)s visited to %(slug_url)s')
        return message % {'ip_address': self.ip_address, 'slug_url': slug_url}

    class Meta:
        verbose_name = _('Visitor')
        verbose_name_plural = _('Visitors')
        unique_together = ('ip_address', 'slug_url')
        ordering = ('-created_at',)


class Favorite(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    objects = DefaultManager()

    def __str__(self):
        title = self.post.title
        title = title if len(title) <= 50 else '%s ...' % title[:50]
        return _('%(post)s marked as favorite by %(user)s') % {'post': title, 'user': self.user}

    class Meta:
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')
        unique_together = ('user', 'post')
        ordering = ('-created_at',)


class Gallery(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=200, blank=True, null=True)
    attachment = models.FileField(_('Attachment'), upload_to='attachments/%Y/%m/%d')

    def __str__(self):
        return self.title or self.attachment.name.split('/')[-1]

    class Meta:
        verbose_name = _('Gallery')
        verbose_name_plural = _('Galleries')
        ordering = ('-created_at',)
