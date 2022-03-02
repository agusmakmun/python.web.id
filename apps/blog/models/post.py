# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from updown.models import Vote
from updown.fields import RatingField
from martor.models import MartorField

from apps.blog.models.base import (TimeStampedModel, DefaultManager,
                                   ContentTypeModel)
from apps.blog.models.addons import (Visitor, Favorite)


class PostManager(DefaultManager):

    def published(self):
        """ publish manager for post without `publish` field """
        return super().published()

    def published_public(self):
        """ update publish manager for post """
        queryset = super().published()
        return queryset.filter(publish=True)


class Post(TimeStampedModel, ContentTypeModel):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    description = MartorField(_('Description'))
    tags = models.ManyToManyField('Tag')
    keywords = models.CharField(_('Keywords'), null=True, blank=True,
                                max_length=200, help_text=_('Separate by comma (,)'))
    meta_description = models.TextField(_('Meta Description'), null=True, blank=True)
    is_featured = models.BooleanField(_('Is Featured?'), default=False)
    publish = models.BooleanField(_('Publish'), default=True)
    rating = RatingField(can_change_vote=True)

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('apps.blog:post_detail', kwargs={'slug': self.slug})

    def get_content_type(self):
        """ function to get the content_type object for this model """
        self.content_type = super().get_content_type()
        return self.content_type

    def get_visitors(self):
        """ function to get the queryset of visitors """
        if hasattr(self, 'content_type'):
            content_type = self.content_type
        else:
            content_type = self.get_content_type()
        queries = {'content_type': content_type, 'object_id': self.id}
        return Visitor.objects.published().filter(**queries)

    @property
    def total_visitors(self):
        """ count the total of visitors """
        return self.get_visitors().count()

    def get_favorites(self):
        """ function to get the queryset of favorites """
        if hasattr(self, 'content_type'):
            content_type = self.content_type
        else:
            content_type = self.get_content_type()
        queries = {'content_type': content_type, 'object_id': self.id}
        return Favorite.objects.published().filter(**queries)

    @property
    def total_favorites(self):
        """ count the total of favorites """
        return self.get_favorites().count()

    def delete(self, *args, **kwargs):
        """ run delete action for instanced objects """

        queries = {'content_type__model': 'post', 'object_id': self.id}
        Favorite.objects.filter(**queries).delete()
        Visitor.objects.filter(**queries).delete()
        Vote.objects.filter(**queries).delete()

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ('-created_at',)


class Page(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    description = MartorField(_('Description'))
    STATUS_CHOICES = (
        ('site', _('Site')),
        ('private', _('Private')),
        ('documentation', _('Documentation'))
    )
    status = models.CharField(_('Status'), max_length=20,
                              choices=STATUS_CHOICES, default='site')
    publish = models.BooleanField(_('Publish'), default=True)
    objects = DefaultManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ('-created_at',)
