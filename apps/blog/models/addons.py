# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from apps.blog.models.base import (TimeStampedModel, DefaultManager)


class Visitor(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    headers = models.TextField(_('Headers'), null=True, blank=True)
    ip_address = models.CharField(_('IP Address'), max_length=40)
    object_id = models.BigIntegerField()
    content_type = models.ForeignKey(ContentType, related_name='visitors',
                                     on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = DefaultManager()

    def __str__(self):
        message = _('%(ip_address)s visited to %(content_object)s')
        return message % {'ip_address': self.ip_address,
                          'content_object': self.content_object}

    class Meta:
        verbose_name = _('Visitor')
        verbose_name_plural = _('Visitors')
        unique_together = ('ip_address', 'object_id', 'content_type')
        ordering = ('-created_at',)


class Favorite(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    object_id = models.BigIntegerField()
    content_type = models.ForeignKey(ContentType, related_name='favorites',
                                     on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = DefaultManager()

    def __str__(self):
        title = str(self.content_object)
        title = title if len(title) <= 50 else '%s ...' % title[:50]
        return _('%(title)s marked as favorite by %(user)s') % {'title': title, 'user': self.user}

    class Meta:
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')
        unique_together = ('user', 'object_id', 'content_type')
        ordering = ('-created_at',)


class Gallery(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=200, blank=True, null=True)
    attachment = models.FileField(_('Attachment'), upload_to='attachments/%Y/%m/%d')

    def __str__(self):
        return self.title or self.attachment.name.split('/')[-1]

    class Meta:
        verbose_name = _('Gallery')
        verbose_name_plural = _('Galleries')
        ordering = ('-created_at',)
