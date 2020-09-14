# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# from updown.models import Vote
# from updown.fields import RatingField

from app_blog.models.base import (TimeStampedModel, DefaultManager)
from app_blog.utils.slug import generate_unique_slug


class Post(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    description = models.TextField(_('Description'))
    tags = models.ManyToManyField('Tag')
    keywords = models.CharField(_('Keywords'), null=True, blank=True,
                                max_length=200, help_text=_('Keywords sparate by comma.'))
    meta_description = models.TextField(_('Meta Description'), null=True, blank=True)
    is_featured = models.BooleanField(_('Is Featured?'), default=False)
    publish = models.BooleanField(_('Publish'), default=True)
    # rating = RatingField(can_change_vote=True)

    objects = DefaultManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts_detail', kwargs={'slug': self.slug})

    def get_visitors(self):
        if hasattr(self, 'visitorset'):
            return self.visitorset.published()
        return None

    @property
    def total_visitors(self):
        visitors = self.get_visitors()
        return visitors.count() if visitors else 0

    def get_favorites(self):
        return Favorite.objects.filter(post=self)

    @property
    def total_favorites(self):
        return self.get_favorites().count()

    def save(self, *args, **kwargs):
        """ generate an unique slug """
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Post, self.title)
        else:  # create
            self.slug = generate_unique_slug(Post, self.title)
        super(Post, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ run delete action for instanced objects """

        # votes = Vote.objects.filter(content_type__model='post', object_id=self.id)
        # votes.delete()

        super(Post, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ('-created_at',)


class Page(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    description = models.TextField(_('Description'))
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

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Page, self.title)
        else:  # create
            self.slug = generate_unique_slug(Page, self.title)
        super(Page, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ('-created_at',)
